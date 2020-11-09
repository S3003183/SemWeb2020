import json
import os

alldata = []
directory = 'data/songs'
for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    with open(os.path.join(directory, filename)) as f:
        song = json.load(f)
        data = {}
        data[song[6]['hasValue']['value']] = song
        alldata.append(data)

with open(f"data/songs/all_songs.json", "w") as outfile:
    json.dump(alldata, outfile)

