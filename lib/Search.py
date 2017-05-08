import json
import re
from Track import *

def build_qurey(s, d_query):
    # build description query if exists
    if len(d_query['description']) > 0:
        q = Q("bool",
            must=[
            Q("multi_match", query = d_query['description'], fields=['title', 'lyric', 'artist_name', 'artist_location', 'genres', 'album'], operator='and'),
            ],
        )
        s = s.query(q)

    # build query according to artists if exists
    if len(d_query['artist_name']) > 0:
        s = s.filter(Q('match', artist_name = d_query['artist_name']))
        # s = s.sort('artist_name')


    #build genre filter if exists
    if len(d_query['genre']) > 0:
        print 52
        s = s.filter(Q('match', genres = d_query['genre']))


    # set hightlight in title and text
    # s = s.highlight_options(order='score')
    # s = s.highlight("lyric")
    # s = s.highlight('title')

    print(s.to_dict())
    return s

# Parameters
# ----------
# d_query: dictionary
#     a dictionary that stores every field of the query
#     value string : description, artist_name, artist_location, album
#     value range: duration_l, duration_h, year_l, year_h
#     value list of string: genre
# Returns
# -------
# a list of dictionary
def search(d_query):
    connections.create_connection(hosts=['localhost'])
    Track.init()
    corpusSize = 10000
    s = Track.search()
    s = build_qurey(s,d_query)
    s = s[:corpusSize]  # limit size
    s = s.highlight("*", fragment_size=99999999,
                              pre_tags='<z>', post_tags='</z>')
    results = s.execute()
    return results
    # l_results = []
    # s = s[0:results.hits.total]
    # for track in s:
    #     dict_track = {}
    #     dict_track['id'] = track.meta.id
    #     dict_track['score'] = track.meta.score
    #     dict_track['title'] = track.title
    #     dict_track['lyric'] = track.lyric[0:200]
    #
    #
    #     l_results.append(dict_track)
    # return l_results

d_query = {'description': u'love','artist_name':u'','genre':u''}
print search(d_query)
# print d
