from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
# from music_ontology import get_classlist, get_class_instances, get_description
from data.mo_artist_names import artist_names
# from data.mo_artist_ids_names import artist_ids_names
from wikidata import update_or_create_artist, remove_artist_instance, create_artist, get_musicbraiz_id
import json
import os

all_artists_path = 'data/all_artists.json'

def read_json(path):
    with open(path) as f:
        return json.load(f)


all_artists = read_json(all_artists_path)
abc = get_musicbraiz_id(all_artists['Kevin Dooley'])

update_or_create_artist(all_artists['Johnny Kass'])
# remove_artist_instance("Bertram Ritter")

