#!/usr/bin/env python
# author: @sopier
from flask import render_template, request, redirect, send_from_directory
from flask import make_response # untuk sitemap
from flask import jsonify
from app import app
# untuk find_one based on data id => db.freewaredata.find_one({'_id': ObjectId(file_id)})
# atom feed
from werkzeug.contrib.atom import AtomFeed
from bson.objectid import ObjectId
from bson import json_util
from filters import slugify
import datetime
import pymongo
import json

c = pymongo.Connection()
termsdb = c["terms"]
pdfdb = c["pdfs"]
gsuggestdb = c["gsuggests"]
bsuggestdb = c["bsuggests"]


@app.template_filter()
def slug(s):
    """
    transform words into slug
    usage: {{ string|slug }}
    """
    return slugify(s)

# handle robots.txt file
@app.route("/robots.txt")
def robots():
    # point to robots.txt files
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/")
def index():
    return render_template("index.html")

# just-in-case we need it in the future
class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

@app.route("/stats")
def stats():
    """Return statistics data from mongo."""
    pdfdbnum = pdfdb.pdf.find().count()
    termsdbnum = termsdb.term.find().count()
    gsuggestsnum = gsuggestdb.suggest.find().count()
    bsuggestsnum = bsuggestdb.suggest.find().count()
    resp = make_response(json.dumps({
        'pdf': pdfdbnum,
        'terms': termsdbnum,
        'google_suggest': gsuggestsnum,
        'bing_suggest': bsuggestsnum,
        }, cls=Encoder))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/pdf/api/v1.0/latest")
def get_docs():
    """Return 30 latest data from database."""
    data = [i for i in pdfdb.pdf.find().sort("_id", -1).limit(30)]
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/pdf/api/v1.0/search/<keyword>")
def keyword_search(keyword):
    """Search and return 10 results from database."""
    data = pdfdb.command('text', 'pdf', search=keyword, limit=10)
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/pdf/api/v1.0/search/<keyword>/<page>")
def keyword_search_paging(keyword, page):
    """Search and return 10 results from database."""
    data = pdfdb.command('text', 'pdf', search=keyword, limit=30)
    start = int(page) * 10 - 10
    end = int(page) * 10
    data = [i for i in data['results']][start:end]
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/pdf/api/v1.0/single/<oid>")
def get_single_doc(oid):
    """Search for single data in database."""
    data = pdfdb.pdf.find_one({"_id": ObjectId(oid)})
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/terms/api/v1.0/latest")
def get_terms():
    """Return 30 latest data from database."""
    data = [i for i in termsdb.term.find().sort("_id", -1).limit(30)]
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/terms/api/v1.0/search/<keyword>")
def term_search(keyword):
    """Search and return 30 results from database."""
    data = termsdb.command('text', 'term', search=keyword, limit=30)
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/gsuggests/api/v1.0/latest")
def get_gsuggests():
    """Return 30 latest data from database."""
    data = [i for i in gsuggestdb.suggest.find().sort("_id", -1).limit(30)]
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/gsuggests/api/v1.0/search/<keyword>")
def gsuggests_search(keyword):
    """Search and return 30 latest data from database."""
    data = gsuggestdb.command('text', 'suggest', search=keyword, limit=5)
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/bsuggests/api/v1.0/latest")
def get_bsuggests():
    """Return 30 latest data from database."""
    data = [i for i in bsuggestdb.suggest.find().sort("_id", -1).limit(30)]
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route("/bsuggests/api/v1.0/search/<keyword>")
def bsuggests_search(keyword):
    """Search and return 30 latest data from database."""
    data = bsuggestdb.command('text', 'suggest', search=keyword, limit=5)
    resp = make_response(json.dumps({'results': data},
                                    default=json_util.default))
    resp.headers["Content-Type"] = "application/json"
    return resp
