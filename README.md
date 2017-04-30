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
## new

##
getCorpus.py:  get raw information from hdf5 file   ==> raw_music_corpus.json
getlyrics.py: get lyrics information according to train data.txt file  ==> music_corpus.json
mxm.py: get lyrics information and genre information using API to MXM website ==> new_music_corpus.json

## Corpus format (1000 songs from Hdf5 file)
{"1":{
    msdID: string,
    trackID: string,
    songID: string,
    title: string, song's name,
    year: int,
    song_hotttnesss: float,
    artistName: string,
    artistID: string,
    artist_familiarity:
    artist_hotttnesss:
    artist_location:
    duration: seconds,
    release: album name,
    similar_artists: array
    lyrics:


  },
  "2":{

  },
  ...
}
