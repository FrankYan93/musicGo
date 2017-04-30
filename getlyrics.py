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
    with open('mxm_dataset_train.txt', 'r') as fp:
        words = fp.readline()
        while words.startswith("#"):
            words = fp.readline()
        words = words[1:]
        print words
        wd = words.split(",")

    # pp.pprint(music)
    #
    # with open('music_corpus.json', 'w') as fp:
    #     json.dump(music, fp)

if __name__ == '__main__':
    main()
