# -*- coding: UTF-8 -*-
import os
import sys
import hdf5_getters
import numpy as np
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)
music = {}

def main():
    rootdir = '/Users/Jerry/desktop/2017_Spring/COSI 132A/project/MillionSongSubset/data'
    number = 0
    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            fileroot = os.path.join(subdir, f)
            h5 = hdf5_getters.open_h5_file_read(fileroot)
            # numSongs = hdf5_getters.get_num_songs(h5)
            # if numSongs>1:
            #     print fileroot, numSongs, "\n"
            # above code has checked song is 1 for all h5 file
            getters = filter(lambda x: x[:4] == 'get_', hdf5_getters.__dict__.keys())

            getters = np.sort(getters)
            songidx = 0
            number = number + 1
            song = {}
            # print them
            for getter in getters:
                try:
                    res = hdf5_getters.__getattribute__(getter)(h5,songidx)
                except AttributeError, e:
                    if summary:
                        continue
                    else:
                        print e
                        print 'forgot -summary flag? specified wrong getter?'
                if res.__class__.__name__ == 'ndarray':
                    song[getter[4:]] = list(res)
                    # print getter[4:]+": shape =",res.shape
                else:
                    # print getter[4:]+":",res
                    song[getter[4:]] = str(res)
                # song[getter[4:]] = res

            h5.close()
            music[number] = song
            # print song

    pp.pprint(music)

    with open('raw_music_corpus.json', 'w') as fp:
        json.dump(music, fp, indent=4)

if __name__ == '__main__':
    main()
