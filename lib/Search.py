import json
import re
from lib.Track import *

def build_qurey(title, artist, genre, album, lyric):
    # build description query if exists
    if (len(lyric) > 0):
        q = Q("bool",
            must=[
            Q("multi_match", query=lyric, fields=['title', 'text'], operator='and'),
            ],
        )
        s = s.query(q)

    # build query according to artists if exists
    if (len(artist) > 0):
        print 42
        queries = []
        for name in process_star(starring):
            queries += [Q('match', artist=name)]

        s = s.query(Q('bool', **{
                'should': queries
            }))


    #build genre filter if exists
    if (genre != 'None'):
        print 52
        s = s.filter(Q('match', genre=genre))


    # set hightlight in title and text
    s = s.highlight_options(order='score')
    s = s.highlight("lyric")
    s = s.highlight('title')

    print(s.to_dict())
    return s


def search(title, artist, genre, album, lyric):
    connections.create_connection(hosts=['localhost'])
    Track.init()

    s = Track.search()
    s = build_qurey(title, artist, genre, album, lyric)
    results = s.execute()

    l_results = []
    s = s[0:results.hits.total]
    for doc in s:
        dict_movie = {}
        dict_movie['id'] = doc.meta.id
        dict_movie['score'] = doc.meta.score
        try:
            dict_movie['title'] = process_highlight(doc.meta.highlight.title, doc.title)
        except:
            dict_movie['title'] = doc.title
        try:
            dict_movie['lyric'] = process_highlight(doc.meta.highlight.lyric, doc.text)[0:200]
        except:
            dict_movie['lyric'] = doc.text[0:200]


        l_results.append(dict_movie)
    return l_results

# d = search('la la land', '', 'None', '', '' )
# print d
