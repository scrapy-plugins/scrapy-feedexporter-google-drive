================================
scrapy-feedexporter-google-drive
================================

.. image:: https://img.shields.io/pypi/v/scrapy-feedexporter-google-drive.svg
   :target: https://pypi.org/project/scrapy-feedexporter-google-drive/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/scrapy-feedexporter-google-drive.svg
   :target: https://pypi.org/project/scrapy-feedexporter-google-drive/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/github/license/scrapy-plugins/scrapy-feedexporter-google-drive.svg
   :target: https://github.com/scrapy-plugins/scrapy-feedexporter-google-drive/blob/master/LICENSE
   :alt: License


scrapy-feedexporter-google-drive is a `Scrapy Feed Exporter Storage Backend
<https://docs.scrapy.org/en/latest/topics/feed-exports.html#storage-backends>`_
that allows you to export `Scrapy items
<https://docs.scrapy.org/en/latest/topics/items.html>`_ to Google Drive.

Requirements
============

-   Python 3.9+

Installation
============

.. code-block:: bash

    pip install scrapy-feedexporter-google-drive

Usage
=====

Add this storage backend to the `FEED_STORAGES
<https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES>`_
Scrapy setting:

.. code-block:: python

    FEED_STORAGES = {
        "gdrive": "scrapy_gdrive_exporter.gdrive_exporter.GoogleDriveFeedStorage"
    }

Configure `authentication
<https://developers.google.com/identity/protocols/oauth2/service-account>`_
with a service account, setting ``GDRIVE_SERVICE_ACCOUNT_CREDENTIALS_JSON`` to
the contents of its JSON credentials file:

.. code-block:: python

    GDRIVE_SERVICE_ACCOUNT_CREDENTIALS_JSON = '{"type": "service_account", "project_id": "…", "private_key_id": "…", "private_key": "…", "client_email": "…", "client_id": "…", "auth_uri": "…", "token_uri": "…", "auth_provider_x509_cert_url": "…", "client_x509_cert_url": "…"}'

Give the service account access to the folder where you want to export the
file, by sharing that folder with the service account's email (``client_email``
in the credentials).

Configure in the `FEEDS
<https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds>`_ Scrapy
setting the Google Drive URI where the feed needs to be exported:

.. code-block:: python

    FEEDS = {
        "gdrive://drive.google.com/<folder_id>/<file_name.extension>": {
            "format": "json",
        },
    }

You can get the ``folder_id`` from the address bar while inside the folder:
``https://drive.google.com/drive/folders/<folder_id>``.

Feed options
============

The ``overwrite`` `feed option
<https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-options>`_ is
not supported: every export is stored as a new file, and existing files are not
overwritten. If ``overwrite`` is set to ``True`` or ``False``, a warning is
logged.
