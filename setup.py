from setuptools import setup

setup(
    name='scrapy-google-drive',
    packages=['scrapy_google_drive'],
    install_requires=[
        'scrapy',
        'pydrive2',
    ],
    requires=['scrapy', 'pydrive2']
)