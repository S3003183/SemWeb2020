from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
# from music_ontology import get_classlist, get_class_instances, get_description
from data.mo_artist_names import artist_names
# from data.mo_artist_ids_names import artist_ids_names
from wikidata import update_or_create_artist, remove_artist_instance, create_artist
import json
import os

all_songs_path = 'data/songs/all_songs.json'

def read_json(path):
    with open(path) as f:
        return json.load(f)


all_songs = read_json(all_songs_path)
all_artists = artist_names

update_or_create_artist("Arnaud Thuilliez")

