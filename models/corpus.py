from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
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


if __name__ == '__main__':
    import lxml.etree as ET
    import glob as glob
    from os import path as p
    import os

    # Create an index
    ix = STORAGE.create_index(Excerpt)

    writer = ix.writer()

    for file in glob.glob("../data/these-corpus/data/*.xml"):
        data = ET.parse(file)
        _id = p.basename(file)
        source = data.xpath("//bibl[@type='source']")[0]
        author = (source.xpath(".//persName[@xml:lang='fr']/text()") + ["Anonyme"])[0]
        title = source.xpath("./title/text()")[0]
        ref = source.xpath("./biblScope/text()")[0]
        body = " ".join(data.xpath("//w/text()"))
        lemmatized = " ".join(data.xpath("//w/@lemma"))
        lemmas = " ".join(data.xpath("//w[contains('NOMcom|NOMpro|ADJqua|VER|ADV', @pos)]/@lemma"))
        anas = " ".join(data.xpath("//w[@ana]/@lemma"))
        tags = data.xpath("@ana")[0].replace("#", "")
        bibls = " ".join(data.xpath("//bibl[not(@type='source')]/@ref"))
        writer.add_document(
            id=_id,
            body=body,
            lemmatized=lemmatized,
            author=author,
            title=title,
            ref=ref,
            lemmas=lemmas,
            anas=anas,
            tags=tags,
            bibliography=bibls
        )
    writer.commit()
