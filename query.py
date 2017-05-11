# Web App for Query
from flask import *
from flask_session import Session
import json
from json2html import *
import re
# from flask_paginate import Pagination
from heapq import *
from collections import defaultdict
from math import *
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Q
# from lib.Track import *
from lib.Search import search, search_track
with open('music_corpus.json', 'r') as opened:
    the_corpus = json.loads(opened.read())
corpusSize = len(the_corpus)
connections.create_connection(hosts=['localhost'])

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
cache = {}  # cache dict for current result


# Being more formal, we should use environment variable here.
# But now we just want to make it simple.
baseurl = "http://0.0.0.0:5000/"

# Here is a useful tool I found. And I did some modification.
# Originally posted by Dan Jacob on 2010-06-17 @ 05:03 and filed in Template Tricks
# This is a nl2br (newline to <BR>) filter, adapted from the Jinja2 example here:
# http://jinja.pocoo.org/2/documentation/api#custom-filters
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


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
    return render_template('query.html', baseurl=baseurl)


@app.route('/query/<k>')
def article(k):
    # print "cache:",cache
    return render_template("target_article.html", table=Markup(json2html.convert(cache[k.encode('utf-8')])))

@app.route('/query', methods=['GET'])
def sortby():
    # print "request.args",request.args
    if 'more' not in session:
        if 'hot' in request.args:
            print 'hot'
            return newQuery(request, 'hot')
        elif 'dance' in request.args:
            print 'dance'
            return newQuery(request, 'dance')
        else:
            return "invalid url or not required parameters"
    else:
        if 'hot' in request.args:
            print 'hot'
            return moreLikeThisQuery('hot')
        elif 'dance' in request.args:
            print 'dance'
            return moreLikeThisQuery('dance')
        else:
            return "invalid url or not required parameters"


@app.route('/query/', methods=['POST', 'GET'])
def query():
    if 'docId' in session and session['docId']:
        return moreLikeThisQuery()

    page = request.args.get('page', type=int, default=1)
    # print 'page:', page
    results = {}
    if request.method == 'GET':

        if 'recentResultIds' in session:
            for i in set(session['recentResultIds']):
                results[i] = the_corpus[i]
                results[i]['lyric'] = nl2br(results[i]['original_lyrics'])
        return render_template('SERP.html', results=list(results.iteritems()), noMatch=False, page=page, per_page=10, score=session['resultScore'], baseurl=baseurl)
    return newQuery(request)


@app.route('/query/more/<k>')
def moreLikeThis(k):
    currentId = session['recentResultIds'][int(k.encode('utf-8'))]
    # print currentId
    # print the_corpus[currentId]['title'],
    # the_corpus[currentId]['original_lyrics']
    session['docId'] = currentId
    return redirect(url_for('query'), code=307)


def moreLikeThisQuery(flag = None):
    if not flag:
        cache.clear()
        results = []
        page = 1
        # clear session when post
        session['resultScore'] = None
        session['recentResultIds'] = None
        response = search_track(session['docId'])
        session['latesetDocId'] = session['docId']
        session['more'] = 1
        del session['docId']
    else:
        response = search_track(session['latesetDocId'],flag)
    return getResult(response)



def newQuery(request, flag=None):
    if 'more' in session:
        del session['more']
    if not flag:
        cache.clear()
        # clear session when post
        session['resultScore'] = None
        session['recentResultIds'] = None
        print request.form
        session['latestForm'] = request.form
        response = search(request.form)
        return getResult(response)
    else:
        response = search(session['latestForm'], flag)
        return getResult(response)


def getResult(response):
    results = []
    page = 1
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
    if resultLen == 0:
        return render_template('SERP.html', results=results, noMatch=True, baseurl=baseurl)
    else:
        for i in results:
            i[1]['lyric'] = nl2br(i[1]['lyric'])
            cache[i[0].encode('utf-8')] = json.dumps(i[1].to_dict())
        return render_template('SERP.html', results=results, noMatch=False, page=page, per_page=10, score=session['resultScore'], baseurl=baseurl)


app.secret_key = '\x1a\xb0\x06\x8c\xc4+\xb1\xdbm\xe1t?\xad\x14\xd5\xb1\xf8,\x1e\xa2\x82\xd3\xc7\x96'
if __name__ == "__main__":
    app.run(debug=True)

        # qDict = {'album':u'',
        #         'max_longitude':u'',
        #         'min_longitude':u'',
        #         'description':u'',
        #         'title':u'',
        #         'artist_name':u'',
        #         'min_latitude':u'',
        #         'lyric':u'',
        #         'max_duration':u'',
        #         'year':u'',
        #         'genre':u'',
        #         'min_duration':u'',
        #         'max_latitude':u'',
        #         'artist_location':u''}
