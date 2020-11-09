import json
import os

alldata = {}
directory = 'data/artists'
for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    with open(os.path.join(directory, filename)) as f:
        song = json.load(f)
        alldata[filename.replace('.json', '')] = song

with open(f"data/artists/all_artists.json", "w") as outfile:
    json.dump(alldata, outfile)

