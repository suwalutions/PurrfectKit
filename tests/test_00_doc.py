import pytest
from purrfectmeow.meow.felis import Document

@pytest.fixture
def sample_document():
    page_content = "Something in the way she moves"
    metadata = {"key": "something"}
    return Document(page_content, metadata)

@pytest.fixture
def empty_document():
    page_content = ""
    metadata = {}
    return Document(page_content, metadata)


# test __init__

def test_init_valid():
    doc = Document("Meow, World", {"source": "purr~"})
    assert doc.page_content == "Meow, World"
    assert doc.metadata == {"source": "purr~"}

def test_init_empty_page_content():
    doc = Document("", {"source": "purr~"})
    assert doc.page_content == ""
    assert doc.metadata == {"source": "purr~"}

def test_init_empty_metadata():
    doc = Document("Meow, World", None)
    assert doc.page_content == "Meow, World"
    assert doc.metadata == {}


# test __repr__

def test_repr(sample_document):
    assert repr(sample_document) == "Document(page_content='Something in the way she moves', metadata={'key': 'something'})"

def test_repr_empty(empty_document):
    assert repr(empty_document) == "Document(page_content='', metadata={})"

# test __getitem__

def test_getitem_page_content(sample_document):
    assert sample_document['page_content'] == "Something in the way she moves"

def test_getitem_metadata(sample_document):
    assert sample_document['metadata'] == {'key': 'something'}

def test_getitem_invalid_key(sample_document):
    with pytest.raises(KeyError, match="everything is not a valid key. Use 'page_content' or 'metadata'."):
        sample_document['everything']


# test to_dict

def test_to_dict(sample_document):
    assert sample_document.to_dict() == {'page_content': 'Something in the way she moves', 'metadata': {'key': 'something'}}

def test_to_empty(empty_document):
    assert empty_document.to_dict() == {'page_content': '', 'metadata': {}}


# test multi scenario

@pytest.mark.parametrize("page_content, metadata, any_dict", [
    # normal case
    ("Attracts me like no other lover", {'no': 1}, {'page_content': 'Attracts me like no other lover', 'metadata': {'no': 1}}),

    # empty case
    ("", {}, {'page_content': '', 'metadata': {}}),

    # None metadata
    ("Something in the way she woos me", None, {'page_content': 'Something in the way she woos me', 'metadata': {}}),
], ids=["normal", "empty", "none"])
def test_to_dict_various(page_content, metadata, any_dict):
    doc = Document(page_content, metadata)
    assert doc.to_dict() == any_dict

