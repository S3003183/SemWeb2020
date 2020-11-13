from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
import os
from main import read_json, all_artists_path
from wikidata import get_all_songs, get_song_id, get_artist_name

######### Member variables #########

sparql_url = "http://dbtune.org/musicbrainz/sparql"
class_url = "http://purl.org/ontology/mo/MusicArtist"
object_url = "http://dbtune.org/musicbrainz/resource/artist/006e2063-9d33-4530-be4e-8dfce0b88352"


######### Functions #########
def run_sparql_query(url, query, return_format):
    sparql = SPARQLWrapper(url)

    sparql.setQuery(query)
    sparql.setReturnFormat(return_format)
    return sparql.query().convert()

def get_classlist(sparql_url):
    get_classlist_query = """
    SELECT DISTINCT ?class
    WHERE { [] a ?class }
    ORDER BY ?class
        """
    return run_sparql_query(sparql_url, get_classlist_query, JSON)    

def get_class_instances(class_url):
    get_classlist_query = f"""
    SELECT DISTINCT ?instance
    WHERE {{ ?instance a <{class_url}> }}
    ORDER BY ?instance
    """
    return run_sparql_query(sparql_url, get_classlist_query, JSON)  

def get_description(object_url):
    get_instace_description_query = f""" 
    SELECT DISTINCT ?property ?hasValue ?isValueOf
    WHERE {{
      {{ <{object_url}> ?property ?hasValue }}
      UNION
      {{ ?isValueOf ?property <{object_url}> }}
    }}
    ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf
    """
    return run_sparql_query(sparql_url, get_instace_description_query, JSON)

# def get_class_instance_labels(class_url):
#     get_class_instance_labels_query = f"""
#     SELECT DISTINCT ?instance ?instanceLabel
#     WHERE {{
#      {{?instance a <http://purl.org/ontology/mo/MusicArtist>}}
#     UNION 
#     {{?instance rdfs:label ?instanceLabel}}
#     }}
#     ORDER BY ?instance
#     """
#     instances = get_class_instances(class_url)
#     instance_labels = []
#     # for instance in instances:


#     return instance_labels

######### Main #########
def collect_artists_data():
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

def collect_artists_songs():
    all_artists = read_json(all_artists_path)
    for artist_name, artist in all_artists.items():
        if os.path.exists(f'data/songs/artists/{artist_name}'):
            continue
        all_songs = get_all_songs(artist)
        for song in all_songs:
            song_url = get_song_id(song['isValueOf']['value'])
            # song_url = f"http://dbtune.org/musicbrainz/resource/track/{id}"
            song_obj = get_description(song_url)

            for data_prop in song_obj['results']['bindings']:
                if data_prop['property']['value'] == "http://www.w3.org/2000/01/rdf-schema#label":
                    filename=data_prop['hasValue']['value']
                    filename = filename.replace('/', '') 
                    if not os.path.exists(f'data/songs/artists/{artist_name}'): 
                        os.makedirs(f'data/songs/artists/{artist_name}')
                    with open(f"data/songs/artists/{artist_name}/{filename}.json", "w+") as outfile:
                        json.dump(song_obj, outfile)   

def combine_song_jsons_per_artist():
    alldata = {}
    root_dir = 'data/songs/artists'
    for artist_dir_name in os.listdir(root_dir):
        path_to_artist_dir = os.path.join(root_dir, artist_dir_name)
        for filename in os.listdir(path_to_artist_dir):
            print(os.path.join(path_to_artist_dir, filename))
            with open(os.path.join(path_to_artist_dir, filename)) as f:
                song = json.load(f)
                alldata[filename.replace('.json', '')] = song

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

combine_artist_songs_into_one_object()