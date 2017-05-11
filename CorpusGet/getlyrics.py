# -*- coding: UTF-8 -*-
import os
import sys
import hdf5_getters
import numpy as np
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)
music = {}
mapping = {}

def main():
    rootdir = '/Users/Jerry/desktop/2017_Spring/COSI 132A/project/'
    # nn = 0
    with open('mxm_dataset_train.txt', 'r') as fp:
        for line in fp:
            if line.startswith("%"):
                words = line[1:]
                wd = words.split(",") #staring with 0
            elif not line.startswith("#"):
                # nn = nn + 1
                signs = line.split(",")
                word = signs[2:]
                mapping[signs[0]] = word
    # print nn

    # with open('mxm_dataset_test.txt', 'r') as fp:
    #     for line in fp:
    #         if line.startswith("%"):
    #             words = line[1:]
    #             wd = words.split(",") #staring with 0
    #         elif not line.startswith("#"):
    #             signs = line.split(",")
    #             word = signs[2:]
    #             if not signs[0] in mapping:
    #                 nn = nn + 1
    #                 mapping[signs[0]] = word
    #
    # print nn

    with open('raw_music_corpus.json', 'r') as fp:
        music = json.load(fp)
    # number = 0
    for song in music:
        trackID = music[song]["track_id"]
        music[song]["lyrics"] = []
        if trackID in mapping:
            lyrics = []
            for word in mapping[trackID]:
                ins = word.split(":")
                s = wd[int(ins[0])]
                s = s + ":" + ins[1]
                lyrics.append(s)
            music[song]["lyrics"] = lyrics
            # number = number + 1
            # print mapping[trackID]
    # print number
    pp.pprint (music)

    # pp.pprint(music)
    #
    with open('music_corpus.json', 'w') as fp:
        json.dump(music, fp, indent=4)

if __name__ == '__main__':
    main()
