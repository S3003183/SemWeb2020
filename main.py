from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def run_sparql_query(url, query, return_format):
    sparql = SPARQLWrapper(url)

    sparql.setQuery(query)
    sparql.setReturnFormat(return_format)
    return sparql.query().convert()



wikidata_url = "https://query.wikidata.org/sparql"
wikidata_query = """
    SELECT ?releasetype ?releasetypeLabel
    WHERE {?releasetype wdt:P279 wd:Q2431196 .
           service wikibase:label { bd:serviceParam wikibase:language "en". }
          }

    """

# mo_url = "http://dbtune.org/bbc/peel/sparql/"
mo_url = "http://dbtune.org/musicbrainz/sparql"
# mo_url = "http://dbtune.org/musicbrainz/snorql/"
mo_query = """
SELECT DISTINCT ?class
WHERE { [] a ?class }
ORDER BY ?class
    """

wikidata_results = run_sparql_query(url = wikidata_url, query=wikidata_query, return_format=JSON)
mo_results = run_sparql_query(url = mo_url, query=mo_query, return_format=JSON)

results_df = pd.json_normalize(mo_results['results']['bindings'])
print(results_df[['class.value']])