from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
import os

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
instances_url = "http://purl.org/ontology/mo/Track"
instances = get_class_instances(instances_url)['results']['bindings']
for instance in instances:
    object_url = instance['instance']['value']
    object_description = get_description(object_url)

    results_df = object_description['results']['bindings']
    filename=object_description['results']['bindings'][6]['hasValue']['value']
    filename = filename.replace('/', '')
    with open(f"data/songs/{filename}.json", "w") as outfile:
        json.dump(results_df, outfile)