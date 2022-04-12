import logging

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from scrapy.extensions.feedexport import BlockingFeedStorage


logger = logging.getLogger(__name__)


class GoogleDriveFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):
        gauth = GoogleAuth()

        gauth.LoadCredentialsFile("creds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()

        # Save the current credentials to a file
        gauth.SaveCredentialsFile("creds.txt")
        self.drive = GoogleDrive(gauth)  
        self.uri = uri

    def _store_in_thread(self, file):
        """
        Uploads a file to google drive
        """
        file.seek(0)
        path = self.uri.replace('gdrive://', '')

        gfile = self.drive.CreateFile(
            {
                'title': path
            }
        )
        # Read file and set it as the content of this instance.
        gfile.SetContentString(file.read().decode("utf-8"))
        gfile.Upload() # Upload the file.
