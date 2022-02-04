import pickle
import os
import logging

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from scrapy.extensions.feedexport import BlockingFeedStorage

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file'
]


logger = logging.getLogger(__name__)


class GoogleDriveFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):
        self.uri = uri
        logger.info("Starting GoogleDriveFeedStorage")

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('drive', 'v3', credentials=creds)


    def _store_in_thread(self, file):
        """
        Uploads a file to google drive
        """
        file.seek(0)
        path = self.uri.replace('gdrive://', '')

        media = MediaFileUpload(
            file.name,
            mimetype="text/plain",
            resumable=True
        )

        body = {
            'name': path,
        }

        try:
            new_file = self.service.files().create(
                body=body,
                media_body=media,
            ).execute()

            file_title = new_file.get('name')
            if file_title == path:
                print(f"File is uploaded \nTitle : {file_title}")
        except HttpError as error:
            print(f'An error occurred: {error}')
