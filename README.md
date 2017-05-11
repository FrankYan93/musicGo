# musicGo  
## Author
**[Jiadong Yan](https://github.com/FrankYan93)**  
**[Jiaming Xu](https://github.com/Dragoncell)**  
**[Xinyi Jiang](https://github.com/xyjiang94)**  

## Latest Modify Date
**May 10th 2017**

## Functionality
1. basic search: search the description on title, lyric, album and artist_name
2. advanced search: search on every possible filed, including title, lyric, album, artist_name, location, duration, genres, year
3. More like this: search similar tracks, based on its title, lyric and similarity of the artist
4. Sorting:
  - default: sort by relevance
  - sort by song hotness
  - sort by danceability


## Getting Started
0. install homebrew
1. `brew tap homebrew/science`
2. `brew install hdf5`
3. `pip install Cython`
4. install Tables by `sudo pip install git+https://github.com/PyTables/PyTables`
5. install other packages mentioned in **Dependency**.
6. build elasticsearch as mentioned in **Build Elasticsearch**
7. type `redis-server` in terminal
8. `python query.py`

## Build Elasticsearch
- `cp lib/name_syn.txt [your elasticsearch path]/config/name_syn.txt`
- `cp lib/cat_syn.txt [your elasticsearch path]/config/cat_syn.txt`   
(It is not recommended, but if you really want to let your web application access a folder outside its deployment directory. You need to add permission in java.policy file. Details see http://stackoverflow.com/questions/10454037/java-security-accesscontrolexception-access-denied-java-io-filepermission)
- open elasticsearch server:
  `cd elasticsearch-<version>  
  ./bin/elasticsearch`  

- run `python ./lib/buildElaticSearch.py`
- build time: 9s
- use another terminal to run `redis-server`

## Functionality
1. We support baisc title and lyrics search for whatever you want!  
2. We support many filters, like duration, artist, genre, etc!  
3. You can find hotttest songs near your position!!!  

## Dependency
- hdf5
- Cython
- Flask
- PyTables
- elasticsearch_dsl
- elasticsearch
- json
- math
- redis

## Code submitted by
Jiadong Yan

## Corpus Source
- https://labrosa.ee.columbia.edu/millionsong/
- https://www.musixmatch.com/

### Corpus format (1000 songs from Hdf5 file)
{"1":{  
    "trackID": string,  
    "title": (song's name) string,  
    "year": int,  
    "song_hotttnesss": float,  
    "artistName": string,  
    "artistID": string,  
    "artist_hotttnesss": float,  
    "artist_location":String,  
    "duration": (seconds) int,  
    "release": (album name) string,  
    "similar_artists": a list of (artistID) string,  
    "lyrics": string,  
    "artist_longitude": float,  
    "artist_latitude": float,  
    "artist_location": String,  
    "danceability": float  
  },  
  "2":{

  },  
  ...  
}


## Modules

### static folder:
css file and images

### templates folder:
* search box view
* search results view

### music_corpus.json:
the corpus of 10000 songs, the format is described above.

### lib/Track.py
This file defines a doc_tpye track and its field, as well as the analyzers

### lib/buildElaticSearch.py
This file builds the elasticsearch index from the music_corpus.json

### lib/Search.py
This file takes different types of query as input, builds elasticsearch search query, search in elastic and return the results. It is responsible of search on all fields and sort by specific features.

### getCorpus.py:  
get raw information from hdf5 file   ==> raw_music_corpus.json

### getlyrics.py:
get lyrics information according to train data.txt file  ==> music_corpus.json

### mxm.py:
get lyrics information and genre information using API to MXM website ==> new_music_corpus.json

### cleanCorpus.py:
get desired attributes from the corpus
