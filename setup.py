from setuptools import setup

setup(
    name='scrapy-google-drive',
    packages=['scrapy_google_drive'],
    install_requires=[
        'scrapy',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'tabulate',
        'pydrive',
    ],
    requires=['scrapy',]
)