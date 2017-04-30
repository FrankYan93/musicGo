# get music information and store to elasticsearch
from lib.Track import *
from elasticsearch import *


def build(l):
    connections.create_connection(hosts=['localhost'])
    Track.init()

    track_list = []
    for info in l:
        track = Track(title = title, lyric = lyric, singer = singer, genre = genre, album = album)
        track_list.append(track)

    es = Elasticsearch()
    helpers.bulk(es,  (d.to_dict(include_meta=True) for d in track_list ))
