import json
import re
from Track import *

def build_qurey(s, d_query, flag):
    # build description query if exists
    if len(d_query['description']) > 0:
        q = Q("bool",
            must=[
            Q("multi_match", query = d_query['description'], fields=['title', 'lyric', 'artist_name', 'artist_location', 'album'], operator='or'),
            ],
        )
        s = s.query(q)

    if len(d_query['title']) > 0:
        s = s.query(Q('match', title = d_query['title']))

    if len(d_query['lyric']) > 0:
        s = s.query(Q('match', lyric = d_query['lyric']))

    if len(d_query['artist_name']) > 0:
        s = s.query(Q('match', artist_name = d_query['artist_name']))

    if len(d_query['artist_location']) > 0:
        s = s.query(Q('match', artist_location = d_query['artist_location']))

    if len(d_query['album']) > 0:
		s = s.query(Q('match', album = d_query['album']))

    s = s.query(Q("match_all"))

    if len(d_query['genre']) > 0:
		s = s.filter(Q('match', genres = d_query['genre']))

    if len(d_query['year']) > 0:
        year = int(d_query['year'])
        s = s.filter(Q('term', year = year))

    if len(str(d_query['min_duration'])) > 0 and len(str(d_query['max_duration'])) > 0:
        l = int(str(d_query['min_duration']))
        h = int(str(d_query['max_duration']))
        s = s.filter('range', duration={'lte': h, 'gte': l})

    if len(str(d_query['min_latitude'])) > 0 and len(str(d_query['max_latitude'])) > 0:
        l = int(str(d_query['min_latitude']))
        h = int(str(d_query['max_latitude']))
        s = s.filter('range', artist_latitude={'lte': h, 'gte': l})

    if len(str(d_query['min_longitude'])) > 0 and len(str(d_query['max_longitude'])) > 0:
        l = int(str(d_query['min_longitude']))
        h = int(str(d_query['max_longitude']))
        s = s.filter('range', artist_longitude={'lte': h, 'gte': l})

    if flag == 'hot':
        s = s.sort(
        { "song_hotttnesss" : "desc" }
        )
    elif flag == 'dance':
        s = s.sort(
        { "danceability" : "desc" }
        )

    corpusSize = 40
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
def search(d_query,flag = 'none'):
    connections.create_connection(hosts=['localhost'])
    Track.init()

    s = Track.search()
    s = build_qurey(s,d_query,flag)

    results = s.execute()
    return results


def build_track_qurey(s,track_id):
    queries = []
    track = Track.get(id=track_id)
    description = track.title + track.lyric
    queries.append( Q("multi_match", query = description, fields=['title', 'lyric', 'album'], operator='or') )
    queries.append( Q('match', similar_artists = track.track_id) )
    for query in queries:
        s = s.query(Q('bool', **{
                'should': queries
            }))
    corpusSize = 40
    s = s[:corpusSize]  # limit size
    s = s.highlight("*", fragment_size=99999999,
                              pre_tags='<z>', post_tags='</z>')
    return s

def search_track(track_id):
    connections.create_connection(hosts=['localhost'])
    Track.init()

    s = Track.search()
    s = build_track_qurey(s,track_id)

    results = s.execute()
    return results

if __name__ == '__main__':
    d_query = {'title': u'',
                'lyric': u'',
            'album': u'',
            'max_longitude': u'', 'min_longitude': u'',
            'description': u'',
            'max_duration': u'',
            'artist_name': u'',
            'min_latitude': u'',
            'year': u'',
            'genre': u'','min_duration': u'','max_latitude': u'','artist_location': u''}
    res = search(d_query,'hot')
    # print len(res) ,'\n\n\n',res[0].meta.id
    # res = search_track(5883)
    print len(res) ,'\n\n\n',res[0].meta.id
    for song in res:
        print song.song_hotttnesss
