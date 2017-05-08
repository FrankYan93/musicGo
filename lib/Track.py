from elasticsearch_dsl import *
from elasticsearch_dsl.connections import connections

import os
# name_filter = token_filter('synonym',type = "synonym", synonyms_path = "analysis/name_syn.txt" )

name_anl = analyzer('name_anl',
    tokenizer="standard",
    analyzer="snowball",
    filter=["standard", "lowercase", "snowball", token_filter('name_filter', 'synonym', synonyms_path = "name_syn.txt")],
)

cat_anl = analyzer('name_anl',
    tokenizer="standard",
    analyzer="snowball",
    filter=["standard", "lowercase", "snowball", token_filter('cat_filter', 'synonym', synonyms_path = "cat_syn.txt")],
)

text_anl = analyzer('text',
    tokenizer="standard",
    analyzer="snowball",
    filter=["standard", "lowercase", "snowball", "stop", "stemmer"],
)


class Track(DocType):
    track_id = Keyword()
    title = Text(analyzer=text_anl)
    lyric = Text(analyzer=text_anl)
    artist_name = Text(analyzer=name_anl)
    artist_id = Keyword()
    artist_location = Text(analyzer=text_anl)
    duration = Float()
    genres = Text(
        analyzer=cat_anl,
        fields={'genres': Text()}
    )
    album = Text(analyzer=text_anl)
    year = Integer()
    similar_artists = Keyword(
        fields={'artist_id': Keyword()}
        )
    artist_latitude = Float()
    artist_longitude = Float()
    song_hotttnesss = Float()
    danceability = Float()


    class Meta:
        index = 'music'
        doc_type = 'track'

    def save(self, ** kwargs):
        return super(Track, self).save(** kwargs)




if __name__ == '__main__':

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
    # movies.create()
    Track.init()

    test = Track(title = 'test', lyric = 'Hello World!!!')
    test.meta.id = 1
    print type(test), test, test.title
    test.save()

    test2 = Track.get(id=1)
    print type(test2), test2, test2.title
