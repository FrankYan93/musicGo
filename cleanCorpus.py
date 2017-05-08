# -*- coding: UTF-8 -*-
import os
import sys
import hdf5_getters
import numpy as np
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)
mm = {}

def main():
    with open('new_music_corpus.json', 'r') as fp:
        music = json.load(fp)

    for song in music:
        music[song].pop('energy',None)
        music[song].pop('artist_mbid',None)
        music[song].pop('artist_7digitalid',None)
        music[song].pop('artist_playmeid',None)
        music[song].pop('track_7digitalid',None)
        music[song].pop('release_7digitalid',None)
        music[song].pop('song_id',None)
        # music[song].pop('song_id',None)

        music[song]["genre"] = []
        try:
            g = music[song]["primary_genres"]["music_genre_list"]
            # print g
            for i in g:
                # print i
                ge = i["music_genre"]["music_genre_name"]
                music[song]["genre"].append(ge)
        except:
            print "wrong"

        try:
            g = music[song]["secondary_genres"]["music_genre_list"]
            for i in g:
                ge = i["music_genre"]["music_genre_name"]
                music[song]["genre"].append(ge)
        except:
            print "wrong"
        music[song].pop('primary_genres',None)
        music[song].pop('secondary_genres',None)
        music[song].pop('artist_familiarity',None)
        music[song].pop('artist_hotttnesss',None)
        music[song].pop('loudness',None)
        mm[int(song)] = music[song]
        print song
        print music[song]["genre"]

    # print music
    with open('music_corpus.json', 'w') as fp:
        json.dump(mm, fp, indent=4)

if __name__ == '__main__':
    main()
