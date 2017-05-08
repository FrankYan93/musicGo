# get music information and store to elasticsearch
from Track import *
from elasticsearch import *
import json


def import_dict (path):
    json_file = open(path, 'r')
    track_dict = json.loads(json_file.read())
    json_file.close()
    return track_dict

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
        try:
            latitude = int(track_dict[key]["artist_latitude"])
        except:
            latitude = 0
        try:
            longitude = int(track_dict[key]["artist_longitude"])
        except:
            longitude = 0
        try:
            song_hotttnesss = int(track_dict[key]["song_hotttnesss"])
        except:
            song_hotttnesss = 0

        track = Track(track_id = track_dict[key]["track_id"], title = track_dict[key]["title"], lyric = track_dict[key]["original_lyrics"], artist_name = track_dict[key]["artist_name"], artist_id = track_dict[key]["artist_id"], artist_location = track_dict[key]["artist_location"], duration = track_dict[key]["duration"], genres = track_dict[key]["genre"], album = track_dict[key]["release"], year = track_dict[key]["year"], similar_artists = track_dict[key]["similar_artists"],artist_latitude = latitude,artist_longitude = longitude,song_hotttnesss = song_hotttnesss ,danceability = track_dict[key]["danceability"])
        track.meta.id = track_dict[key]["track_id"]
        track_list.append(track)
    print len(track_list)
    es = Elasticsearch()
    helpers.bulk(es,  (d.to_dict(include_meta=True) for d in track_list ))

if __name__ == '__main__':
    json_path = "music_corpus.json"
    build(json_path)
