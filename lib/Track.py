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
    title = Text(analyzer=text_anl)
    lyric = Text(analyzer=text_anl)
    singer = Text(
        analyzer=name_anl,
        fields={'star': Text()}
    )
    genre = Text(
        analyzer=cat_anl,
        fields={'raw': Text()}
    )
    album = Text(analyzer=text_anl)


    class Meta:
        index = 'music'

    def get_text(self):
        return self.text


if __name__ == '__main__':

    connections.create_connection(hosts=['localhost'])

    music = Index('music')

    # define custom settings
    music.settings(
        number_of_shards=1,
        number_of_replicas=0
    )

    # register a doc_type with the index
    music.doc_type(Track)

    # delete the index, ignore if it doesn't exist
    # music.delete(ignore=404)

    # create the index in elasticsearch
    # movies.create()
    Track.init()

    test = Track(title = 'test', text = 'Hello World!!!')
    test.meta.id = 1
    print type(test), test, test.get_text()
    test.save()

    test2 = Track.get(id=1)
    print type(test2), test2, test2.get_text()
