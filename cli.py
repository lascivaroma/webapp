from .app import app, ROOT_DIR
from .models.corpus import STORAGE, Excerpt
import lxml.etree as ET
import glob as glob
from os import path as p
import os


@app.cli.command("build-index")
def feed():
    # Create an index
    ix = STORAGE.create_index(Excerpt)

    writer = ix.writer()

    for file in glob.glob(os.path.join(ROOT_DIR, "data", "these-corpus", "data", "*.xml")):
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
        bibls = " ".join(data.xpath("//bibl[not(@type='source')]/@ref")).replace("#", "")
        adamsPage = "".join(data.xpath("//bibl[@ref='#adams']/biblScope/text()")).strip()
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
            bibliography=bibls,
            adamsPage=adamsPage
        )
    writer.commit()
