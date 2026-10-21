import logging
import os
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def parse_gdrive_uri(uri):
    """Takes in uri and returns folder_id and file_name in a dictionary"""
    extracted_params = {}
    try:
        # parse uri
        parsed_uri = urlparse(uri)

        # split by / so we can get folder_id and file_name
        splitted = parsed_uri.path.split("/", 2)

        # check for valid uri conditions
        valid_netloc = parsed_uri.netloc.lower() == "drive.google.com"
        has_path = bool(parsed_uri.path)
        has_folder_and_file = bool(len(splitted) == 3 and splitted[1] and splitted[2])

        if not valid_netloc or not has_path or not has_folder_and_file:
            return None

        folder_id = splitted[1]
        file_name = splitted[2]
        file_name_without_ext, ext = os.path.splitext(file_name)  # noqa: PTH122

        if not file_name_without_ext or not ext:
            return None

        # return folder_id and file_name in a dictionary
        extracted_params["folder_id"] = folder_id
        extracted_params["file_name"] = file_name
        return extracted_params
    except Exception:
        logger.exception("Could not parse %r", uri)
        return None
