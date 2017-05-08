import json
import re
from Track import *

def build_qurey(s, d_query):
    # build description query if exists
    if len(d_query['description']) > 0:
        q = Q("bool",
            must=[
            Q("multi_match", query = d_query['description'], fields=['title', 'lyric', 'artist_name', 'artist_location', 'album'], operator='and'),
            ],
        )
        s = s.query(q)

    # build query according to artists if exists
    if len(d_query['artist_name']) > 0:
        s = s.query(Q('match', artist_name = d_query['artist_name']))
        # s = s.sort('artist_name')

    # build query according to artists if exists
    if len(d_query['artist_location']) > 0:
        s = s.query(Q('match', artist_location = d_query['artist_location']))

    # build query according to artists if exists
    if len(d_query['album']) > 0:
		s = s.query(Q('match', album = d_query['album']))


    s = s.query(Q("match_all"))

    #build genre filter if exists
    if len(d_query['genre']) > 0:
		s = s.filter(Q('match', genres = d_query['genre']))

    # build query according to artists if exists
    if len(d_query['year']) > 0:
        year = int(d_query['year'])
        s = s.filter(Q('term', year = year))


    corpusSize = 10000
    s = s[:corpusSize]  # limit size
    s = s.highlight("*", fragment_size=99999999,
                              pre_tags='<z>', post_tags='</z>')

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

    s = Track.search()
    s = build_qurey(s,d_query)

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

if __name__ == '__main__':
    d_query = {'album': u'',
            'max_longitude': u'', 'min_longitude': u'',
            'description': u'',
            'max_duration': u'',
            'artist_name': u'',
            'min_latitude': u'',
            'year': u'',
            'genre': u'','min_duration': u'','max_latitude': u'','artist_location': u''}
    res = search(d_query)
    print len(res),'\n\n\n',res
