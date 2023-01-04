# Google Drive Exporter for Scrapy
[Scrapy feed export storage backend](https://doc.scrapy.org/en/latest/topics/feed-exports.html#storage-backends) for Google Drive.

## Requirements
-  Python 3.8+

## Installation
```bash
pip install git+https://github.com/scrapy-plugins/scrapy-feedexporter-google-drive
```
## Usage
* Add this storage backend to the [FEED_STORAGES](https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES) Scrapy setting. For example:
    ```python
    # settings.py
    FEED_STORAGES = {'gdrive': 'scrapy_gdrive_exporter.gdrive_exporter.GoogleDriveFeedStorage'}
    ```
* Configure [authentication](https://developers.google.com/identity/protocols/oauth2/service-account) with service account like following:
  
  For example,
  ```python
  GDRIVE_SERVICE_ACCOUNT_CREDENTIALS_JSON = '{ "type": "service_account", "project_id": "project_id here", "private_key_id": "private_key_id here", "private_key": "private_key here", "client_email": "client_email here", "client_id": "client_id here", "auth_uri": "auth_uri here", "token_uri": "token_uri here", "auth_provider_x509_cert_url": "auth_provider_x509_cert_url here", "client_x509_cert_url": "client_x509_cert_url here" }'
    ```
* Give access of the folder (where you want to export the file) to the service account used in previous step. This can be done by sharing that folder with the service account's email (available in credentials as `client_email`)
* Configure in the [FEEDS](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds) Scrapy setting the Google Drive URI where the feed needs to be exported.

    ```python
    FEEDS = {
        "gdrive://drive.google.com/<folder_id>/<file_name.extension>": {
            "format": "json"
        }
    }
    ```
  - You can get the `folder_id` of the folder from the address bar, while being inside that folder.
    - e.g: `https://drive.google.com/drive/folders/<folder id is here>`
## Feed Options
- The `overwrite` [feed option](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-options) is not supported by this exporter.
  - If it's set to `True` or `False`, a warning will be logged.
  - The current behavior of this exporter is that the exported file is always stored as a new file. They are not overwrited.