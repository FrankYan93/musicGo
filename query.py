# Web App for Query
from flask import *
from flask.ext.session import Session
import json
from json2html import *
import re
from flask_paginate import Pagination
from heapq import *
from collections import defaultdict
from math import *
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Q
# from lib.Track import *
from lib.Search import search
with open('music_corpus.json', 'r') as opened:
    the_corpus = json.loads(opened.read())
corpusSize = len(the_corpus)
connections.create_connection(hosts=['localhost'])

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
# Here is a useful tool I found. And I did some modification.
# Originally posted by Dan Jacob on 2010-06-17 @ 05:03 and filed in Template Tricks
# This is a nl2br (newline to <BR>) filter, adapted from the Jinja2 example here:
# http://jinja.pocoo.org/2/documentation/api#custom-filters
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
cache = {} # cache dict for current result
baseurl = "http://0.0.0.0:5000/"

@app.template_filter()
@evalcontextfilter
def nl2br(value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', Markup('<br>'))
                          for p in _paragraph_re.split(value))
    result = Markup(result)
    return result


@app.route('/')
def entryPage():
    session.clear()
    return render_template('query.html', baseurl = baseurl)


@app.route('/query/<k>')
def article(k):
    # return render_template('target_article.html',article=the_corpus[k])
    return render_template("target_article.html", table=Markup(json2html.convert(cache[k.encode('utf-8')])))

@app.route('/query/', methods=['POST', 'GET'])
def query():
    if 'docId' in session and session['docId']:
        return moreLikeThis()

    page = request.args.get('page', type=int, default=1)
    # print 'page:', page
    results = {}
    if request.method == 'GET':
        if 'recentResultIds' in session:
            for i in set(session['recentResultIds']):
                results[i] = the_corpus[i]
                results[i]['text'] = nl2br(results[i]['text'])
        pagination = Pagination(page=page, total=len(
            results), per_page=10, prev_label='Prev', next_label='Next', css_framework='foundation')
        return render_template('SERP.html', results=list(results.iteritems()), noMatch=False, pagination=pagination, page=page, per_page=10, score=session['resultScore'], baseurl = baseurl)
    return newQuery(request)

@app.route('/query/more/<k>')
def moreLikeThis(k):
    print 71
    for e in session:
        print e
    print 74
    currentId = session['recentResultIds'][int(k.encode('utf-8'))]
    print currentId
    print the_corpus[currentId]['title'], the_corpus[currentId]['original_lyrics']
    # session['query'] = the_corpus[currentId]['title'] +\
    #     " " + the_corpus[currentId]['text']
    session['docId'] = currentId
    return redirect(url_for('query'), code=307)

def moreLikeThis():
    pass

def newQuery(request):
    cache.clear()
    results = []
    page = 1
    # clear session when post
    session['resultScore'] = None
    session['recentResultIds'] = None
    # print request.form
    response = search(request.form)
    if response:
        session['recentResultIds'] = []
        session['resultScore'] = []
    # for e in response['hits']:
    #     print e
    for e in response['hits']['hits']:
        results.append([])
        results[-1].append(e['_id'])
        results[-1].append(e['_source'])
        if 'highlight' in e:
            for ele in e['highlight']:
                results[-1][1][ele] = e['highlight'][ele][0]
        results[-1][1]['score'] = e['_score']
        results[-1][1]['title'] = Markup(results[-1][1]['title'])
        session['recentResultIds'].append(e['_id'])
        session['resultScore'].append(e['_score'])
    artist_query = []
    resultLen = len(results)
    for e in session:
        print e,session[e]
    if resultLen == 0:
        return render_template('SERP.html', results=results, noMatch=True, baseurl = baseurl)
    else:
        for i in results:
            i[1]['lyric'] = nl2br(i[1]['lyric'])
            cache[i[0].encode('utf-8')] = json.dumps(i[1].to_dict())
        # limit 10 per page
        pagination = Pagination(page=page, total=resultLen, per_page=10,
                                prev_label='Prev', next_label='Next', css_framework='foundation')
        return render_template('SERP.html', results=results, noMatch=False, pagination=pagination, page=page, per_page=10, score=session['resultScore'], baseurl = baseurl)


app.secret_key = '\x1a\xb0\x06\x8c\xc4+\xb1\xdbm\xe1t?\xad\x14\xd5\xb1\xf8,\x1e\xa2\x82\xd3\xc7\x96'
if __name__ == "__main__":
    app.run(debug=True)
