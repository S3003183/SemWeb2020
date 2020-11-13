from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
# from music_ontology import get_classlist, get_class_instances, get_description
from data.mo_artist_names import artist_names
# from data.mo_artist_ids_names import artist_ids_names
from wikidata import *
import json
import os

all_artists_path = 'data/all_artists.json'
songs_dir_path = 'data/songs/artist_allsongs'

def read_json(path):
    with open(path) as f:
        return json.load(f)


all_artists = read_json(all_artists_path)
artist_name = 'Teresa Catalán'
artist = all_artists[artist_name]
artist_in_path_name = artist_name.replace('/', '')
songs = read_json(f'{songs_dir_path}/{artist_in_path_name}.json')
artist_entity = retrieve_artist_from_wikidata_if_exists(artist_name)
artist_wikidata_id = get_artist_wikidata_id(artist_entity)
songs_iter = next(iter(songs.items()))


#update_or_create_artist(artist)
update_or_create_song(songs_iter[1]['results']['bindings'], artist_wikidata_id, artist_name)
# justin_id = get_artist_wikidata_id(justin)
# baby = retrieve_song_from_wikidata_if_exists('Baby', justin_id)
#update_or_create_artist(all_artists['Teresa Catalán'])
# update_or_create_artist(all_artists['Don Omar y Hec-tor El Bambino'])
# remove_artist_instance("Teresa Catalán")

