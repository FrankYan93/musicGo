# Jiaming Xu contribute this code

# -*- coding: UTF-8 -*-
from urllib import urlopen
import pprint
import json
import copy

pp = pprint.PrettyPrinter(indent=4)

rootapi = "https://www.mediawiki.org/w/api.php"


with open('music_corpus.json', 'r') as fp:
    music = json.load(fp)

song = "2"
if song == "2":
    title = music[song]["title"].encode('utf-8')

    ins = urlopen(rootapi + "?action=%s" % title).read()
    # ins = json.loads(url)
    print ins
    # if ins["message"]["header"]["status_code"] == 200:

# with open('new_music_corpus.json', 'w') as fp:
#     json.dump(music, fp, indent=4)
# print number
