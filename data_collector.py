import json
import os
from main import ALL_ARTISTS_PATH
from wikidata import get_all_songs, get_song_id
from music_ontology import *

######### Functions #########
# Reads a json file stored in path
def read_json(path):
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return {}

# Collect data of arists in MusicBrainz ontology
# Store each artist as json file in data/artists
def collect_artists_data():
    if not os.path.exists(f'data'): 
        os.makedirs(f'data')
    if not os.path.exists(f'data/artists'): 
        os.makedirs(f'data/artists')
    instances_url = "http://purl.org/ontology/mo/MusicArtist"
    instances = get_class_instances(instances_url)['results']['bindings']
    for instance in instances:
        object_url = instance['instance']['value']
        object_description = get_description(object_url)

        results_df = object_description['results']['bindings']
        for data_prop in results_df:
            if data_prop['property']['value'] == "http://www.w3.org/2000/01/rdf-schema#label":
                filename=data_prop['hasValue']['value']
                filename = filename.replace('/', '')  
                with open(f"data/artists/{filename}.json", "w") as outfile:
                    json.dump(results_df, outfile)
                print(f"{filename}.json created") 

# Combines each artist json in data/artists to a json file where artists name is key.  
def combine_artist_data():
    alldata = {}
    directory = 'data/artists'
    for filename in os.listdir(directory):
        print(os.path.join(directory, filename))
        with open(os.path.join(directory, filename)) as f:
            song = json.load(f)
            alldata[filename.replace('.json', '')] = song
    print('Writing data to data/all_artists.json')
    with open(f"data/all_artists.json", "w") as outfile:
        json.dump(alldata, outfile)

# Collect data of songs for each artist on MusicBrainz ontology
# Store each artists songs as json file in data/songs/artists/<artist name>
def collect_artists_songs():
    if not os.path.exists(f'data/songs'): 
        os.makedirs(f'data/songs')
    if not os.path.exists(f'data/songs/artists'): 
        os.makedirs(f'data/songs/artists')
    all_artists = read_json(ALL_ARTISTS_PATH)
    for artist_name, artist in all_artists.items():
        if os.path.exists(f'data/songs/artists/{artist_name}'):
            continue
        all_songs = get_all_songs(artist)
        for song in all_songs:
            song_url = get_song_id(song['isValueOf']['value'])
            song_obj = get_description(song_url)

            for data_prop in song_obj['results']['bindings']:
                if data_prop['property']['value'] == "http://www.w3.org/2000/01/rdf-schema#label":
                    filename=data_prop['hasValue']['value']
                    filename = filename.replace('/', '') 
                    if not os.path.exists(f'data/songs/artists/{artist_name}'): 
                        os.makedirs(f'data/songs/artists/{artist_name}')
                    with open(f"data/songs/artists/{artist_name}/{filename}.json", "w") as outfile:
                        json.dump(song_obj, outfile)  
                    print(f"data/songs/artists/{artist_name}/{filename}.json created") 

# Combines each artists songs from json in data/songs/artists/<artist name>. 
# Store songs of an artist as json in data/songs/artist_allsongs/<artist_name>.json
def combine_song_jsons_per_artist():
    if not os.path.exists(f'data/songs/artist_allsongs'): 
        os.makedirs(f'data/songs/artist_allsongs')
    root_dir = 'data/songs/artists'
    for artist_dir_name in os.listdir(root_dir):
        # Ignore hidden files
        if not artist_dir_name.startswith('.'):
            alldata = {}
            path_to_artist_dir = os.path.join(root_dir, artist_dir_name)
            for filename in os.listdir(path_to_artist_dir):
                print(os.path.join(path_to_artist_dir, filename))
                with open(os.path.join(path_to_artist_dir, filename)) as f:
                    song = json.load(f)['results']['bindings']
                    alldata[filename.replace('.json', '')] = song
            print(f"Writing data to data/songs/artist_allsongs/{artist_dir_name}.json")
            with open(f"data/songs/artist_allsongs/{artist_dir_name}.json", "w") as outfile:
                json.dump(alldata, outfile)

def combine_artist_songs_into_one_object():
    alldata = {}
    directory = 'data/songs/artist_allsongs'
    for filename in os.listdir(directory):
        print(os.path.join(directory, filename))
        with open(os.path.join(directory, filename)) as f:
            song = json.load(f)
            alldata[filename.replace('.json', '')] = song

    with open(f"data/songs/all_song_data.json", "w") as outfile:
        json.dump(alldata, outfile)
