import pickle
import os
import logging

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
from googleapiclient.http import MediaFileUpload

from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


logger = logging.getLogger(__name__)


class GoogleDriveFeedStorage(BlockingFeedStorage):

    def __init__(self):
        # self.uri = uri
        logger.info("Starting GoogleDriveFeedStorage")
        # print("Starting GoogleDriveFeedStorage")

    # def get_gdrive_service(self):
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
        # return Google Drive API service
        # return build('drive', 'v3', credentials=creds)
        self.service = build('drive', 'v3', credentials=creds)


    def _store_in_thread(self, file):
        """
        Creates a folder and upload a file to it
        """
        # file.seek(0)
        # authenticate account
        # service = self.get_gdrive_service()
        # folder details we want to make
        folder_metadata = {
            "name": "TestFolderBerg",
            "mimeType": "application/vnd.google-apps.folder"
        }
        # create the folder
        folder = self.service.files().create(body=folder_metadata, fields="id").execute()
        # get the folder id
        folder_id = folder.get("id")
        print("Folder ID:", folder_id)
        logger.info(f"Folder ID: {folder_id}")
        # upload a file text file
        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": "test.txt",
            "parents": [folder_id]
        }
        # upload
        media = MediaFileUpload("test.txt", resumable=True)
        test_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created, id:", test_file.get("id"))


# if __name__ == '__main__':
#     # main()
#     upload_files()
