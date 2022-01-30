import os.path
from flask import render_template, request, url_for
from whoosh.qparser import QueryParser
from whoosh.query import Term, And, Every
import lxml.etree as ET

from ..app import app, index, Excerpt, ROOT_DIR, ExcerptPropertyNames


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
    return url_for(".search", bibliography=bibl[0].replace("#", ""))


def url_for_adams_page(_, page):
    return url_for(".search", adamsPage=page[0])


ns = ET.FunctionNamespace('http://foo.bar')
ns.prefix = 'foo'
ns['get_tags'] = get_tags
ns['url_for_tags'] = url_for_tags
ns['url_for_bibl'] = url_for_bibl
ns['url_for_adamsPage'] = url_for_adams_page


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


@app.route("/index")
def all_page():
    page = request.args.get("page", 1, int)
    with index.searcher() as searcher:
        results = searcher.search_page(Every(), pagenum=page, pagelen=20, sortedby="adamsPage")
        return render_template(
            "all_pages.html",
            results=results
        )


@app.route("/search")
def search():
    query = request.args.get("q", None)
    allow = None
    q = None
    page = request.args.get("page", 1, int)

    facets = list([
        (key, value)
        for key in request.args.keys()
        for value in request.args.getlist(key)
        if key in {"tags", "anas", "author", "bibliography", "lemmas"} and value is not None
    ])

    if query:
        qp = QueryParser("body", schema=index.schema)
        q = qp.parse(query)

    if facets:
        allow = And(
            [
                Term(key, val)
                for key, val in facets
            ]
        )
    if q or facets:
        with index.searcher() as searcher:
            results = searcher.search_page(q or allow, pagenum=page, pagelen=20, filter=allow, )
            facet_tags = results.results.key_terms("tags", numterms=10)
            facet_anas = results.results.key_terms("anas", numterms=10)
            facet_author = results.results.key_terms("author", numterms=10)
            facet_adams = results.results.key_terms("adamsPage", numterms=10)
            facet_bibliography = results.results.key_terms("bibliography", numterms=10)
            facet_lemmas = results.results.key_terms("lemmas", numterms=10)
            return render_template(
                "search.html",
                query=query, results=results,
                facets={
                    "tags": {"data": facet_tags, "nice": "Tags"},
                    "anas": {"data": facet_anas, "nice": "Central lemma"},
                    "author": {"data": facet_author, "nice": "Author"},
                    "adamsPage": {"data": facet_adams, "nice": "Adams' page"},
                    "bibliography": {"data": facet_bibliography, "nice": "Bibliography"},
                    "lemmas": {"data": facet_lemmas, "nice": "Lemma encountered"},
                },
                current_params=list([
                    (key, value)
                    for key in request.args.keys()
                    for value in request.args.getlist(key)
                    if key in {"tags", "anas", "author", "q", "bibliography", "lemmas", "adamsPage"}
                ])
            )
    else:
        with index.searcher() as searcher:
            results = searcher.search_page(Every(), pagenum=page, pagelen=20, sortedby="adamsPage")
            facet_tags = results.results.key_terms("tags", numterms=10)
            facet_anas = results.results.key_terms("anas", numterms=10)
            facet_author = results.results.key_terms("author", numterms=10)
            return render_template(
                "search.html",
                query=query, results=results,
                facets={
                    "tags": {"data": facet_tags, "nice": "Tags"},
                    "anas": {"data": facet_anas, "nice": "Central lemma"},
                    "author": {"data": facet_author, "nice": "Author"}
                }
            )


@app.route("/indexes")
@app.route("/indexes/<index_type>")
def indexes(index_type=None):
    if index_type and index_type in ExcerptPropertyNames:
        with index.reader() as _index:
            return render_template(
                "indexes.html",
                nice=ExcerptPropertyNames[index_type],
                index_type=index_type,
                keywords=_index.field_terms(index_type)
            )
    else:
        return render_template("indexes_list.html", categories=ExcerptPropertyNames)
