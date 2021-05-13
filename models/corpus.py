from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.filedb.filestore import FileStorage
import os.path

INDEX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../index_dir")
INDEX_NAME = "excerpts"

STORAGE = FileStorage(INDEX_DIR)


class Excerpt(SchemaClass):
    id = ID(stored=True)
    body = TEXT(stored=True)
    lemmatized = TEXT(stored=True)
    author = ID(stored=True, sortable=True)
    title = ID(stored=True)
    ref = STORED
    lemmas = KEYWORD(stored=True)
    anas = KEYWORD(stored=True, sortable=True)
    tags = KEYWORD(stored=True, sortable=True)
    bibliography = KEYWORD(stored=True)
    adamsPage = NUMERIC(stored=True)