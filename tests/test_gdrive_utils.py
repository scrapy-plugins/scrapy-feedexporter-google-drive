import pytest

from scrapy_gdrive_exporter.gdrive_utils import parse_gdrive_uri


@pytest.mark.parametrize(
    "input, expected",
    [
        ("gdrive://drive.google.com/", None),
        (
            "gdrive://drive.google.com/folder_id/myfile.json",
            {"folder_id": "this_is_folder_id", "file_name": "myfile.json"},
        ),
        ("gdrive://drive.google.com//some_text//some_more_text.txt", None),
        ("gdrive://drive.google.com//some_text///some_more_text.txt", None),
    ],
)
def test_parse_gdrive_uri(input, expected):
    result = parse_gdrive_uri(input)
    assert result == expected
