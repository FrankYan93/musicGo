# musicGo  
## Author
**[Jiadong Yan](https://github.com/FrankYan93)**  
**[Jiaming Xu](https://github.com/Dragoncell)**  
**[Xinyi Jiang](https://github.com/xyjiang94)**  

## Getting Started
0. install homebrew
1. `brew tap homebrew/science`
2. `brew install hdf5`
3. `pip install Cython`
4. install Tables by `sudo pip install git+https://github.com/PyTables/PyTables`
5. install other packages mentioned in **Dependency**.
6. build elasticsearch as mentioned in **Build Elasticsearch**
7. `python query.py`

## Latest Modify Date
**May 10th 2017**

## Resources

## Functionality

## Dependency
- hdf5
- Cython
- Flask
- PyTables
- elasticsearch_dsl
- elasticsearch
- json
- math
- re

## Corpus
- getCorpus.py:  get raw information from hdf5 file   ==> raw_music_corpus.json
- getlyrics.py: get lyrics information according to train data.txt file  ==> music_corpus.json
- mxm.py: get lyrics information and genre information using API to MXM website ==> new_music_corpus.json

## Corpus format (1000 songs from Hdf5 file)
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

## Build Elasticsearch
- `cp name_syn.txt [your elasticsearch path]/config/name_syn.txt`
- `cp cat_syn.txt [your elasticsearch path]/config/cat_syn.txt`   
(It is not recommended, but if you really want to let your web application access a folder outside its deployment directory. You need to add permission in java.policy file. Details see http://stackoverflow.com/questions/10454037/java-security-accesscontrolexception-access-denied-java-io-filepermission)
- open elasticsearch server:
  `cd elasticsearch-<version>  
  ./bin/elasticsearch`  

- run `python ./lib/buildElaticSearch.py`
- build time: 9s
- use another terminal to run `redis-server`
