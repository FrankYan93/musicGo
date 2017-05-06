# musicGo  
## Author
**Jiadong Yan**  
**Jiaming Xu**  
**Xinyi Jiang**  

## Getting Started
0. install homebrew
1. `brew tap homebrew/science`
2. `brew install hdf5`
3. `pip install Cython`
4. install Tables by `sudo pip install git+https://github.com/PyTables/PyTables`

## Date
## Resources
## Functionality
## Dependency
- hdf5
- Cython
- Flask
- PyTables
- elasticsearch_dsl
- elasticsearch
- flask_paginate
- json
- math
- re

## new

##
getCorpus.py:  get raw information from hdf5 file   ==> raw_music_corpus.json
getlyrics.py: get lyrics information according to train data.txt file  ==> music_corpus.json
mxm.py: get lyrics information and genre information using API to MXM website ==> new_music_corpus.json

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

## build elasticsearch corpusSize
open elasticsearch server:
`cd elasticsearch-<version>
./bin/elasticsearch`

run `python ./lib/buildElaticSearch.py`
