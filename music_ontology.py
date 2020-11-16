from SPARQLWrapper import SPARQLWrapper, JSON

######### Member variables #########
sparql_url = "http://dbtune.org/musicbrainz/sparql"

######### Functions #########
# Execute a SPARQL query on DBTune MusicBrainz ontology
def run_sparql_query(url, query, return_format):
    sparql = SPARQLWrapper(url)

    sparql.setQuery(query)
    sparql.setReturnFormat(return_format)
    return sparql.query().convert()

# Retrieve a list of classes in MusicBrainz ontology
def get_classlist(sparql_url):
    get_classlist_query = """
    SELECT DISTINCT ?class
    WHERE { [] a ?class }
    ORDER BY ?class
        """
    return run_sparql_query(sparql_url, get_classlist_query, JSON)    

# Retrieve a list of instances for a particular class in MusicBrainz ontology
def get_class_instances(class_url):
    get_classlist_query = f"""
    SELECT DISTINCT ?instance
    WHERE {{ ?instance a <{class_url}> }}
    ORDER BY ?instance
    """
    return run_sparql_query(sparql_url, get_classlist_query, JSON)  

# Retrieve a list of properties for a particular class instance in MusicBrainz ontology
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

