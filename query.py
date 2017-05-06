# Web App for Query
from flask import *
import json
import re
from flask_paginate import Pagination
from heapq import *
from collections import defaultdict
from math import *
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Q
# from lib.Track import *
# from lib.Search import *
with open('music_corpus.json', 'r') as opened:
    the_corpus = json.loads(opened.read())
corpusSize = len(the_corpus)
connections.create_connection(hosts=['localhost'])

app = Flask(__name__)

# Here is a useful tool I found. And I did some modification.
# Originally posted by Dan Jacob on 2010-06-17 @ 05:03 and filed in Template Tricks
# This is a nl2br (newline to <BR>) filter, adapted from the Jinja2 example here:
# http://jinja.pocoo.org/2/documentation/api#custom-filters
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
cache = {}


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
    return render_template('query.html')


@app.route('/query/<k>')
def article(k):
    # return render_template('target_article.html',article=the_corpus[k])
    return render_template("target_article.html", table=Markup(json2html.convert(cache[k.encode('utf-8')])))

@app.route('/query/', methods=['POST', 'GET'])
def query():
    page = request.args.get('page', type=int, default=1)
    print 'page:', page
    results = {}
    if request.method == 'GET':
        if 'recentResultIds' in session:
            for i in set(session['recentResultIds']):
                results[i] = the_corpus[i]
                results[i]['text'] = nl2br(results[i]['text'])
        pagination = Pagination(page=page, total=len(
            results), per_page=10, prev_label='Prev', next_label='Next', css_framework='foundation')
        return render_template('SERP.html', results=list(results.iteritems()), noMatch=False, pagination=pagination, page=page, per_page=10, score=session['resultScore'])
    return newQuery(request)

def newQuery(request):
    cache.clear()
    results = []
    page = 1
    # clear session when post
    session['resultScore'] = None
    session['recentResultIds'] = None
    try:
        query_string = request.form['query'].strip()
        artist_string = request.form['artist'].strip()
        genre_string = request.form['genre'].strip()
    except KeyError:
        print "key error? It should not happen!"
    print "query_string:", query_string
    print "artist_string:", artist_string
    print "genre_string:", genre_string
    query_terms = []
    query_stop_words = []
    weight = {}
    invalidList = []
    splitedQuery = query_string.split("\"")
    myQueryDict = {}
    search = Track.search()
    for i in range(len(splitedQuery)):
        if i % 2 == 1:
            myQueryDict[i] = {
                "multi_match": {
                    "query":      splitedQuery[i],
                    "type":       "phrase",
                    "operator":   "and",
                    "fields":     ["title", "text"]
                }
            }
        else:
            myQueryDict[i] = {
                "multi_match": {
                    "query":      splitedQuery[i],
                    "operator":   "and",
                    "fields":     ["title", "text"]
                }
            }
        if splitedQuery[i]:
            search = search.query(Q(myQueryDict[i]))

    qs = Q('match', artist={'query': artist_string})
    if artist_string:
        search = search.query(qs)
    if genre_string:
        search = search.filter('match', genres={'query': genre_string})
    search = search[:corpusSize + 1]  # limit size
    search = search.highlight("*", fragment_size=99999999,
                              pre_tags='<z>', post_tags='</z>')
    print(search.to_dict())
    response = search.execute()
    if response:
        session['recentResultIds'] = []
        session['resultScore'] = []
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
    print "resultLen:", resultLen
    if resultLen == 0:
        return render_template('SERP.html', results=results, noMatch=True)
    else:
        for i in results:
            i[1]['text'] = nl2br(i[1]['text'])[4:]  # remove the first <br> tag
            cache[i[0].encode('utf-8')] = json.dumps(i[1].to_dict())
        # limit 10 per page
        pagination = Pagination(page=page, total=resultLen, per_page=10,
                                prev_label='Prev', next_label='Next', css_framework='foundation')
        return render_template('SERP.html', results=results, noMatch=False, pagination=pagination, page=page, per_page=10, score=session['resultScore'])


app.secret_key = '\x1a\xb0\x06\x8c\xc4+\xb1\xdbm\xe1t?\xad\x14\xd5\xb1\xf8,\x1e\xa2\x82\xd3\xc7\x96'
if __name__ == "__main__":
    app.run()
