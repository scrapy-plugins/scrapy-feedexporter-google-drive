import json
import logging
import mimetypes

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage

from .gdrive_utils import parse_gdrive_uri

logger = logging.getLogger(__name__)


class GoogleDriveFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, service_account_creds_json, *, feed_options=None):
        if feed_options is None:
            feed_options = {}

        if feed_options and feed_options.get("overwrite") is not None:
            logger.warning(
                "This feed exporter does not support overwrite operation."
                " To suppress this warning, remove the overwrite "
                "option from your FEEDS setting"
            )

        extracted_params = parse_gdrive_uri(uri)
        if not extracted_params:
            raise NotConfigured(
                "Please provide URI according to this format please enter correct path with the format: "
                "'gdrive://drive.google.com/folder_id/file_name.extension'"
            )
        self.folder_id = extracted_params["folder_id"]
        self.file_name = extracted_params["file_name"]
        self.scopes = ["https://www.googleapis.com/auth/drive"]

        try:
            credentials_dict = json.loads(service_account_creds_json, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            self.service = build("drive", "v3", credentials=self.credentials)
        except Exception as e:
            logger.exception(e)
            raise NotConfigured(
                "Please provide valid service account credentials in json string format"
            )

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return cls(
            uri,
            crawler.settings.get("GDRIVE_SERVICE_ACCOUNT_CREDENTIALS_JSON"),
            feed_options=feed_options,
        )

    def _store_in_thread(self, file):
        file.seek(0)
        metadata = {"name": self.file_name, "parents": [self.folder_id]}
        mimetype, encoding = mimetypes.guess_type(self.file_name)
        if not mimetype:
            mimetype = "application/octet-stream"
            logger.warning(
                f"No mimetype found for {self.file_name}, using mimetype={mimetype}"
            )
        media = MediaIoBaseUpload(
            file, chunksize=5 * 1024 * 1024, mimetype=mimetype, resumable=True
        )
        self.service.files().create(body=metadata, media_body=media).execute()
        file.close()
