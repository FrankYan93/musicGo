from elasticsearch_dsl import DocType, Text, Integer, analyzer, token_filter

name_synonym = token_filter('name_synonym',
    type='synonym',
    synonyms_path='name_syn.txt'
)

name_analyzer = analyzer('name_analyzer',
    tokenizer="whitespace",
    filter=["standard", "lowercase", "stop", name_synonym],
)

class Music(DocType):
    title = Text(analyzer='snowball')
    text = Text(analyzer='snowball')
    artist = Text(analyzer=name_analyzer) # important to not include quotes
    genres = Text(analyzer='snowball')#genre_analyzer)
    class Meta:
        index = 'our_music'
        doc_type = 'music'
    def save(self, ** kwargs):
        return super(Music, self).save(** kwargs)
