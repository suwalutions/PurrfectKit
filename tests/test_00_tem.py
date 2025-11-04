import pytest
from unittest.mock import MagicMock
from purrfectmeow.meow.felis import Document, DocTemplate

@pytest.fixture
def sample_metadata():
    return {"artist": "The Beatles", "song": "Something", "released": 1969}

@pytest.fixture
def sample_chunks():
    return [
        "Something in the way she moves",
        "Attracts me like no other lover",
        "Something in the way she woos me"
    ]

@pytest.fixture
def mock_dependencies(mocker):
    mock_uuid = mocker.patch("uuid.uuid4")
    mock_uuid.side_effect = [MagicMock(hex=f"uuid{i+1}") for i in range(10)]

    mock_md5 = mocker.patch("hashlib.md5")
    mock_md5.return_value.hexdigest.side_effect = [f"hash{i+1}" for i in range(10)]

    return mock_uuid, mock_md5

def verify_document(doc, chunk, metadata, index, total_chunks, expected_hash, expected_uuid):
    assert doc.page_content == chunk
    assert doc.metadata['source_info'] == (metadata if metadata is not None else {})

    chunk_info = doc.metadata['chunk_info']
    
    assert chunk_info['chunk_number'] == index + 1
    assert chunk_info['chunk_size'] == len(chunk)
    assert chunk_info['chunk_id'] == expected_uuid
    assert chunk_info['chunk_hash'] == expected_hash
    assert chunk_info['previous_chunk_hash'] == (None if index == 0 else f"hash{index}")
    assert chunk_info['next_chunk_hash'] == (None if index == total_chunks - 1 else f"hash{index + 2}")

@pytest.mark.parametrize(
    "chunks, metadata", 
    [
        (['Something in the way she moves', 'Attracts me like no other lover', 'Something in the way she woos me'], {"artist": "The Beatles", "song": "Something", "released": 1969}),
        (["I don't want to leave her now"], {"artist": "The Beatles", "song": "Something", "released": 1969}),
        (['', 'You know I believe and how'], {"artist": "The Beatles", "song": "Something", "released": 1969}),
        ([], {"artist": "The Beatles", "song": "Something", "released": 1969}),
        (["Somewhere in her smile she knows"], {}),
    ],
    ids=[
        "muliple_chunks",
        "single_chunks",
        "empty_string_chunks",
        "empty_chunks",
        "empty_metadata",
    ]
)
def test_create_template(chunks, metadata, mock_dependencies):
    result = DocTemplate.create_template(chunks, metadata)

    assert len(result) == len(chunks)
    assert all(isinstance(doc, Document) for doc in result)

    for i, doc in enumerate(result):
        verify_document(doc, chunks[i], metadata, i, len(chunks), f"hash{i+1}", f"uuid{i+1}")

def test_create_template_non_string_chunk(sample_metadata, mock_dependencies):
    with pytest.raises(ValueError, match="All elements in 'chunks' must be strings."):
        DocTemplate.create_template([1969, "Something"], sample_metadata)

def test_create_template_string_chunk(sample_metadata, mock_dependencies):
    with pytest.raises(TypeError, match="Expected 'chunks' to be a list, but got str."):
        DocTemplate.create_template("Something in her style she shows me", sample_metadata)

def test_create_template_integer_chunk(sample_metadata, mock_dependencies):
    with pytest.raises(TypeError, match="Expected 'chunks' to be a list, but got int."):
        DocTemplate.create_template(1969, sample_metadata)

def test_create_template_non_metadata(sample_chunks, mock_dependencies):
    with pytest.raises(TypeError, match="Expected 'metadata' to be a dict, but got NoneType."):
        DocTemplate.create_template(sample_chunks, None)

def test_create_template_large_chunks(sample_metadata, mock_dependencies):
    large_chunk = "x" * 10000
    result = DocTemplate.create_template([large_chunk], sample_metadata)
    assert len(result) == 1
    verify_document(result[0], large_chunk, sample_metadata, 0, 1, "hash1", "uuid1")
    assert result[0].metadata['chunk_info']['chunk_size'] == 10000
