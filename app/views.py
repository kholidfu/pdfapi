# author: @sopier

from flask import render_template, request, redirect, send_from_directory
from flask import make_response # untuk sitemap
from flask import jsonify
from app import app
# untuk find_one based on data id => db.freewaredata.find_one({'_id': ObjectId(file_id)})
# atom feed
from werkzeug.contrib.atom import AtomFeed
from bson.objectid import ObjectId
from filters import slugify
import datetime

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

@app.route("/pdf/api/v1.0/latest")
def get_docs():
    """Return 30 latest data from database."""
    data = {
        "results": [
            {
                "name": "sopier",
                "age": 30,
                "occupation": "unclear",
                "address": "sleman"
            },
            {
                "name": "sopier2",
                "age": 20,
                "occupation": "unclear2",
                "address": "mbantul"
                }
            ]}
    return jsonify(data)

@app.route("/pdf/api/v1.0/search/<keyword>")
def keyword_search(keyword):
    """Return 30 latest data from database."""
    data = {
        "results": [
            {
                "name": "sopier",
                "age": 30,
                "occupation": "unclear",
                "address": "sleman"
            },
            {
                "name": "sopier2",
                "age": 20,
                "occupation": "unclear2",
                "address": "mbantul"
                }
            ]}
    return jsonify(data)

@app.route("/terms/api/v1.0/latest")
def get_terms():
    """Return 30 latest data from database."""
    data = {
        "terms": [
            {
                "keyword": "manual"
            },
            {
                "keyword": "automatic"
                }
        ]
    }
    return jsonify(data)

@app.route("/terms/api/v1.0/search/<keyword>")
def term_search(keyword):
    """Return 30 latest data from database."""
    data = {
        "terms": [
            {
                "keyword": "manual"
            },
            {
                "keyword": "automatic"
            }
        ]
    }
    return jsonify(data)

@app.route("/gsuggests/api/v1.0/latest")
def get_gsuggests():
    """Return 30 latest data from database."""
    data = {
        "suggests": [
            {
                "word": "relate"
            },
            {
                "word": "unrelated"
                }
        ]
    }
    return jsonify(data)

@app.route("/gsuggests/api/v1.0/search/<keyword>")
def gsuggests_search(keyword):
    """Return 30 latest data from database."""
    data = {
        "terms": [
            {
                "word": "related"
            },
            {
                "word": "unrelated"
            }
        ]
    }
    return jsonify(data)

@app.route("/bsuggests/api/v1.0/latest")
def get_bsuggests():
    """Return 30 latest data from database."""
    data = {
        "suggests": [
            {
                "word": "relate"
            },
            {
                "word": "unrelated"
                }
        ]
    }
    return jsonify(data)

@app.route("/bsuggests/api/v1.0/search/<keyword>")
def bsuggests_search(keyword):
    """Return 30 latest data from database."""
    data = {
        "terms": [
            {
                "word": "related"
            },
            {
                "word": "unrelated"
            }
        ]
    }
    return jsonify(data)


@app.route("/sitemap.xml")
def sitemap():
    # data = db.freewaredata.find()
    # sitemap_xml = render_template("sitemap.xml", data=data)
    # response = make_response(sitemap_xml)
    # response.headers['Content-Type'] = 'application/xml'

    # return response
    pass

@app.route('/recent.atom')
def recent_feed():
    # http://werkzeug.pocoo.org/docs/contrib/atom/
    # wajibun: id(link) dan updated
    # feed = AtomFeed('Recent Articles',
    #                feed_url = request.url, url=request.url_root)
    # data = datas
    # for d in data:
    #    feed.add(d['nama'], content_type='html', id=d['id'], updated=datetime.datetime.now())
    # return feed.get_response()
    pass
