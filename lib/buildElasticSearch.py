# Xinyi Jiang  contribute this code 
# get music information and store to elasticsearch
from Track import *
from elasticsearch import *
import json
import re
import datetime


def import_dict (path):
    json_file = open(path, 'r')
    track_dict = json.loads(json_file.read())
    json_file.close()
    return track_dict

def convert (s):
    if re.match("^\d+?\.\d+?$", s) is None:
        return 0.0
    else:
        return float(s)

def build(json_path):
    connections.create_connection(hosts=['localhost'])

    music = Index('music')

    # define custom settings
    music.settings(
        number_of_shards=1,
        number_of_replicas=0
    )

    # delete the index, ignore if it doesn't exist
    music.delete(ignore=404)

    # create the index in elasticsearch
    # music.create()
    Track.init()

    track_dict = import_dict(json_path)

    track_list = []
    for key in track_dict:
        latitude = convert(track_dict[key]["artist_latitude"])

        longitude = convert(track_dict[key]["artist_longitude"])

        song_hotttnesss = convert(track_dict[key]["song_hotttnesss"])

        danceability = convert(track_dict[key]["danceability"])

        duration = convert(track_dict[key]["duration"])


        track = Track(track_id = track_dict[key]["track_id"], title = track_dict[key]["title"], lyric = track_dict[key]["original_lyrics"], artist_name = track_dict[key]["artist_name"], artist_id = track_dict[key]["artist_id"], artist_location = track_dict[key]["artist_location"], genres = track_dict[key]["genre"], album = track_dict[key]["release"], year = track_dict[key]["year"], similar_artists = track_dict[key]["similar_artists"],artist_latitude = latitude,artist_longitude = longitude,song_hotttnesss = song_hotttnesss ,danceability = danceability ,  duration = duration)
        track.meta.id = key
        track_list.append(track)

    print len(track_list)
    es = Elasticsearch()
    helpers.bulk(es,  (d.to_dict(include_meta=True) for d in track_list ))

if __name__ == '__main__':
    t1 = datetime.datetime.now()
    json_path = "music_corpus.json"
    build(json_path)
    t2 = datetime.datetime.now()

    print t2 - t1
