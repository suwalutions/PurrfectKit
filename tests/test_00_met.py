import io
import pytest
import time
import subprocess
from unittest.mock import MagicMock
from purrfectmeow.meow.felis import MetaFile

@pytest.fixture
def sample_content():
    return "Something in the way she moves\nAttracts me like no other lover\nSomething in the way she woos me"

MIME_MAP = {
    "csv": "text/csv",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "gif": "image/gif",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    #"md": "",
    "pdf": "application/pdf",
    "png": "image/png",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "txt": "text/plain",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "": "application/octect-stream",
}

@pytest.fixture
def mock_dependencies(mocker):

    mock_os = mocker.patch("os.stat")
    mock_os.return_value.st_size = 100

    mock_magic = mocker.patch("magic.Magic")
    mock_magic.return_value.from_file.side_effect = lambda path: MIME_MAP.get(
        path.split(".")[-1] if "." in path else "", "application/octet-stream"
    )

    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value = MagicMock(stdout="Pages: 1\n")

    mock_hashlib = mocker.patch("hashlib.md5")
    mock_hashlib.return_value.hexdigest.return_value = "mocked_md5_hash"

    mock_time = mocker.patch("time.localtime")
    mock_time.return_value = time.struct_time(
        (2025, 10, 27, 0, 0, 0, 0, 0, 0)
    )
    mock_strftime = mocker.patch("time.strftime")
    mock_strftime.side_effect = lambda fmt, ts=None: "2025-10-27 00:00:00"

    mock_makedirs = mocker.patch("os.makedirs")
    mock_makedirs.return_value = ".cache/tmp"

    mock_remove = mocker.patch("os.remove")
    mock_remove.return_value = None

    yield mock_os, mock_magic, mock_subprocess, mock_hashlib, mock_time, mock_strftime, mock_makedirs, mock_remove

def verify_metadata(metadata, file_name, file_ext):
    assert metadata['file_name'] == file_name
    assert metadata["file_size"] == 100
    assert metadata["file_extension"] == file_ext
    assert metadata["file_created_date"] == "2025-10-27 00:00:00"
    assert metadata["file_modified_date"] == "2025-10-27 00:00:00"
    assert metadata["file_type"] == MIME_MAP.get(file_ext.split(".")[-1])
    assert metadata["description"] == metadata["file_type"]
    assert metadata["total_pages"] == 1
    assert metadata["file_md5"] == "mocked_md5_hash"

def test_get_metadata_from_path_valid(mock_dependencies):
    metadata = MetaFile._get_metadata_from_path("tests/something.txt")
    verify_metadata(metadata, "something.txt", ".txt")

def test_get_metadata_from_path_no_extension(mock_dependencies):
    with pytest.raises(Exception) as excinfo:
        MetaFile._get_metadata_from_path("test")

    assert isinstance(excinfo.value, FileNotFoundError)
    assert "test" in str(excinfo.value)

def test_get_metadata_from_path_wrong_extension(mock_dependencies):
    with pytest.raises(RuntimeError, match="Failed to extract metadata: .*No such file or directory"):
        MetaFile._get_metadata_from_path("tests/test.pdf")

def test_get_metadata_from_path_magic_failure(mock_dependencies):
    mock_dependencies[1].return_value.from_file.side_effect = Exception("Magic error")
    
    metadata = MetaFile._get_metadata_from_path("tests/something.txt")
    
    assert metadata["file_type"] == "unknown"
    assert metadata["description"] == "Could not determine file type: Magic error"

def test_get_metadata_from_path_pdf_subprocess_failure(mock_dependencies):
    mock_dependencies[1].return_value.from_file.return_value = "application/pdf"
    mock_dependencies[2].side_effect = subprocess.CalledProcessError(1, "pdfinfo")
    
    metadata = MetaFile._get_metadata_from_path("tests/something.pdf")
    assert metadata['total_pages'] == "Unknown (pdfinfo not installed or failed)"

# @pytest.mark.parametrize(
#     "file_name", 
#     [
#         ("test.csv"),
#         ("test.doc"),
#         ("test.docx"),
#         ("test.gif"),
#         ("test.jpg"),
#         ("test.pdf"),
#         ("test.png"),
#         ("test.pptx"),
#         ("test.txt"),
#         ("test.xls"),
#         ("test.xlsx"),
#     ], 
#     ids=[
#         "csv", "doc", "docx", "gif", 
#         "jpg", "pdf", "png", "pptx", 
#         "txt", "xls", "xlsx"
#     ]
# )
# def test_get_metadata_from_path_various(file_name, mock_dependencies):
#     file_path = f"test/{file_name}"
#     file_ext = file_name.split("test")[-1]
#     metadata = MetaFile._get_metadata_from_path(file_path)
#     verify_metadata(metadata, file_name, file_ext)

def test_get_metadata_bytesio(sample_content, mock_dependencies):
    byte_data = sample_content.encode('utf-8')
    metadata = MetaFile.get_metadata(io.BytesIO(byte_data), file_name="something.txt")
    verify_metadata(metadata, "something.txt", ".txt")

def test_get_metadata_bytesio_no_name(sample_content, mock_dependencies):
    byte_data = sample_content.encode('utf-8')
    with pytest.raises(ValueError, match="file_name must be provided when using BytesIO"):
        MetaFile.get_metadata(io.BytesIO(byte_data))

def test_get_metadata_invalid_input(mock_dependencies):
    with pytest.raises(TypeError, match="Unsupported file type: int. Expected str, bytes, or BytesIO."):
        MetaFile.get_metadata(123)

def test_get_metadata_empty_file(mock_dependencies):
    text = ""
    byte_data = text.encode('utf-8')
    metadata = MetaFile.get_metadata(io.BytesIO(byte_data), file_name="empty.txt")
    verify_metadata(metadata, "empty.txt", ".txt")