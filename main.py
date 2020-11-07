from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

sparql.setQuery("""
SELECT ?releasetype ?releasetypeLabel
WHERE {?releasetype wdt:P279 wd:Q2431196 .
       service wikibase:label { bd:serviceParam wikibase:language "en". }
      }

""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.json_normalize(results['results']['bindings'])
print(results_df[['releasetype.value', 'releasetypeLabel.value']])