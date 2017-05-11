# Jiaming Xu contribute this code

from urllib import urlopen
import pprint
import json
import copy

pp = pprint.PrettyPrinter(indent=4)

rootapi = "http://api.musixmatch.com/ws/1.1/"
apikey = "&apikey=a6a442aee3216c557ee6e10a09a2ecfd"

with open('raw_music_corpus.json', 'r') as fp:
    music = json.load(fp)

mapping = {}
with open('mxm_779k_matches.txt', 'r') as fp:
    for line in fp:
        if not line.startswith("#"):
            signs = line.split("<SEP>")
            mapping[signs[0]] = signs[3]

# number = 0  7506 songs in mapping
mm = copy.deepcopy(music)

for song in mm:
    trackID = music[song]["track_id"]
    music[song]["primary_genres"] = {}
    music[song]["secondary_genres"] = {}
    music[song]["original_lyrics"] = ""
    if trackID in mapping:
        # number = number + 1
        track_id = mapping[trackID] # in mxm

        #find genre
        url = urlopen(rootapi + "track.get?track_id=%s" % track_id + apikey).read()
        ins = json.loads(url)
        if ins["message"]["header"]["status_code"] == 200:
            lol = ins["message"]
            print song
            music[song]["primary_genres"] = lol["body"]["track"]["primary_genres"]
            music[song]["secondary_genres"] = lol["body"]["track"]["secondary_genres"]

        #find lyrics
        url = urlopen(rootapi + "track.lyrics.get?track.id=%s" % track_id + apikey).read()
        ins = json.loads(url)
        # pp.pprint (ins)
        if ins["message"]["header"]["status_code"] == 200:
            print ins["message"]["body"]["lyrics"]["lyrics_body"]
            music[song]["original_lyrics"] = ins["message"]["body"]["lyrics"]["lyrics_body"]

with open('new_music_corpus.json', 'w') as fp:
    json.dump(music, fp, indent=4)
# print number
