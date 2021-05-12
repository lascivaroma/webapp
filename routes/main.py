import os.path
from flask import render_template, request, url_for
from whoosh.qparser import QueryParser
from whoosh.query import Term
import lxml.etree as ET
from app import app, index, Excerpt, ROOT_DIR


def get_tags(_, tag_list):
    return [
        tag
        for tags in tag_list
        for tag in tags.split()
        if tag
    ]


def url_for_tags(_, tag):
    return url_for(".search", tags=tag[0].replace("#", ""))


def url_for_bibl(_, bibl):
    return url_for(".search", q=bibl[0])


ns = ET.FunctionNamespace('http://foo.bar')
ns.prefix = 'foo'
ns['get_tags'] = get_tags
ns['url_for_tags'] = url_for_tags
ns['url_for_bibl'] = url_for_bibl


XSL = ET.XSLT(
    ET.parse(os.path.join(ROOT_DIR, "statics.xsl"))
)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/read/excerpt/<path:unit>")
def excerpt_read(unit):
    xml = ET.parse(os.path.join(ROOT_DIR, "data", "these-corpus", "data", unit))  # ToDo: sanity check

    return render_template("read.html", content=ET.tostring(XSL(xml), encoding=str).replace("[ ]", ""))


@app.route("/search")
def search():
    query = request.args.get("q", None)
    tags = request.args.get("tags", None)
    bibl = request.args.get("bibl", None)
    allow = None
    q = None
    page = request.args.get("page", 1, int)

    if query:
        qp = QueryParser("body", schema=index.schema)
        q = qp.parse(query)

    if tags:
        allow = Term("tags", tags)

    if q or tags:
        with index.searcher() as searcher:
            results = searcher.search_page(q or allow, pagenum=page, pagelen=20, filter=allow)
            return render_template("search.html", query=query, tags=tags, results=results)

    return render_template("search.html")
