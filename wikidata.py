from wikidataintegrator import wdi_core, wdi_login
from music_ontology import get_description
import time

MUSICIAN_ID = 'Q639669'
INSTANCE_OF_ID = 'P31'
HUMAN_ID = 'Q5'
MUSICIAN = "Musician"
LABEL_PROP_LINK = "http://www.w3.org/2000/01/rdf-schema#label"
MUSIC_BRAINZ_PROP_LINK = 'http://purl.org/ontology/mo/musicbrainz'
MUSIC_BRAINZ_PROP_ID = 'P434'
MAKER_PROP_LINK = 'http://xmlns.com/foaf/0.1/maker'
TRACK_LINK = 'http://dbtune.org/musicbrainz/resource/track/'
SONG_ID = 'Q7366'
PERFORMER_ID = 'P175'
TITLE_ID = 'P1476'
PUBLICATION_DATE_ID = 'P577'
DURATION_ID = 'P2047'
MUSIC_BRAINZ_SONG_PROP_ID = 'P435'
OCCUPATION_ID = 'P106'

# Get WikiData object ids (Q123) for a property.
def get_wikidata_property_values(entity, property_id):
    values = []
    if property_id in entity.wd_json_representation['claims']:
        for i in entity.wd_json_representation['claims'][property_id]:
            if 'id' in i['mainsnak']['datavalue']['value']:
                values.append(i['mainsnak']['datavalue']['value']['id'])
            else:
                values.append(i['mainsnak']['datavalue']['value'])

    return values

def get_instanceOf_ids(entity):
    return get_wikidata_property_values(entity, INSTANCE_OF_ID)

# Retreves WikiData ids of song performers
def get_song_performer_ids(entity):
    return get_wikidata_property_values(entity, PERFORMER_ID)

# Get property ids (P123) for an object
def get_property_ids(entity):
    return entity.wd_json_representation['claims']

def write_to_wikidata(entity, data):
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.update(data)
    entity.write(login_instance)
    

def update_artist(entity, artist_obj):
    existing_occupation_ids = get_wikidata_property_values(entity, OCCUPATION_ID)

    data = entity.statements

    # Set to be musician if not already 
    if MUSICIAN_ID not in existing_occupation_ids:
        # Add occupation musician relation
        data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=OCCUPATION_ID))
    # Set MusicBrainzID if not already set 
    if MUSIC_BRAINZ_PROP_ID not in entity.wd_json_representation['claims']:
        # Add MusicBrainzID relation
        data.append(wdi_core.WDExternalID(value=get_musicbraiz_artist_id(artist_obj), prop_nr=MUSIC_BRAINZ_PROP_ID))
    
    write_to_wikidata(entity, data)
    print(f"Artist {get_artist_name(artist_obj)} has been updated on WikiData server.")

def create_artist(artist_obj):
    data = []
    artist_name = get_artist_name(artist_obj)
    data.append(wdi_core.WDItemID(value=HUMAN_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDExternalID(value=get_musicbraiz_artist_id(artist_obj), prop_nr=MUSIC_BRAINZ_PROP_ID))
    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(artist_name)
    entity.set_description(MUSICIAN)
    
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Artist {artist_name} has been created on WikiData server.")

# Get attribute value by providing property type link ("http://www.w3.org/2000/01/rdf-schema#label")
def get_attribute(artist_obj, attribute_link):
    for data_prop in artist_obj:
        if data_prop['property']['value'] == attribute_link:
            attr_value=data_prop['hasValue']['value']
            return attr_value

def get_artist_name(artist_obj):
    return get_attribute(artist_obj, LABEL_PROP_LINK)

def get_musicbraiz_artist_link(artist_obj):
    return get_attribute(artist_obj, MUSIC_BRAINZ_PROP_LINK)

def get_musicbraiz_artist_id(artist_obj):
    link = get_musicbraiz_artist_link(artist_obj)
    id = link.replace('http://musicbrainz.org/artist/', '')
    return id

def get_musicbraiz_song_link(song_obj):
    return get_attribute(song_obj, MUSIC_BRAINZ_PROP_LINK)

def get_musicbrainz_song_id(song_obj):
    link = get_musicbraiz_song_link(song_obj)
    id = link.replace('http://musicbrainz.org/track/', '')
    return id

def get_all_songs(artist_obj):
    all_songs = []
    for data_prop in artist_obj:
        if data_prop['property']['value'] == MAKER_PROP_LINK and TRACK_LINK in data_prop['isValueOf']['value']:
            all_songs.append(data_prop)
    
    return all_songs

def get_song_name(song_obj):
    return get_artist_name(song_obj)

def get_song_id(track_link):
    id = track_link.replace('db:track/', '')
    return id 

def create_song1(song_obj, artist_obj):
    artist_id_on_wikidata = wdi_core.WDItemEngine.get_wd_search_results(get_artist_name(artist_obj))[0]

    data = []
    # song_name = get_song_name(song_obj)
    song_name = 'Tiengo de calmas'
    artist_name = get_artist_name(artist_obj)
    data.append(wdi_core.WDItemID(value=SONG_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=artist_id_on_wikidata, prop_nr=PERFORMER_ID))
    # data.append(wdi_core.WDString(value=song_name, prop_nr=TITLE_ID))
    # data.append(wdi_core.WDExternalID(value=, prop_nr=PUBLICATION_DATE_ID))
    # data.append(wdi_core.WDString(value=f"{219346} seconds", prop_nr=DURATION_ID))
    data.append(wdi_core.WDExternalID(value=get_musicbrainz_song_id('http://musicbrainz.org/track/1255d2dc-2844-44a9-8bc6-93d870215b89'), prop_nr=MUSIC_BRAINZ_SONG_PROP_ID))


    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(song_name)
    entity.set_description(f"{song_name} by {artist_name}")
    
    
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Song {song_name} by {artist_name} has been created on WikiData server.")
    
def create_song2(song_obj, artist_obj):
    artist_id_on_wikidata = wdi_core.WDItemEngine.get_wd_search_results(get_artist_name(artist_obj))[0]

    data = []
    # song_name = get_song_name(song_obj)
    song_name = 'Tuongs'
    artist_name = get_artist_name(artist_obj)
    data.append(wdi_core.WDItemID(value=SONG_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=artist_id_on_wikidata, prop_nr=PERFORMER_ID))
    # data.append(wdi_core.WDString(value=song_name, prop_nr=TITLE_ID))
    # data.append(wdi_core.WDExternalID(value=, prop_nr=PUBLICATION_DATE_ID))
    # data.append(wdi_core.WDString(value=f"{219346} seconds", prop_nr=DURATION_ID))
    data.append(wdi_core.WDExternalID(value=get_musicbrainz_song_id('http://musicbrainz.org/track/82f775f5-27fe-42e2-af5e-36401bbfc02b'), prop_nr=MUSIC_BRAINZ_SONG_PROP_ID))


    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(song_name)
    entity.set_description(f"{song_name} by {artist_name}")
    
    
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Song {song_name} by {artist_name} has been created on WikiData server.")

def retrieve_artist_from_wikidata_if_exists(artist_name):
    artist_search_result_ids = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    for id in artist_search_result_ids:
        entity = wdi_core.WDItemEngine(wd_item_id=id)
        if MUSICIAN_ID in get_wikidata_property_values(entity, OCCUPATION_ID):
            return entity
    return None

def retrieve_song_from_wikidata_if_exists(song_name, artist_wikidata_id):
    song_search_result_ids = wdi_core.WDItemEngine.get_wd_search_results(song_name)
    for id in song_search_result_ids:
        entity = wdi_core.WDItemEngine(wd_item_id=id)
        if SONG_ID in get_wikidata_property_values(entity, INSTANCE_OF_ID) and artist_wikidata_id in get_wikidata_property_values(entity, PERFORMER_ID): 
            return entity
    return None

def get_artist_wikidata_id(entity):
    return entity.wd_item_id

def update_or_create_artist(artist_obj):
    artist_name = get_artist_name(artist_obj)
    entity = retrieve_artist_from_wikidata_if_exists(artist_name)
    if entity:
        update_artist(entity, artist_obj)
    else: 
        create_artist(artist_obj)

def update_song(entity, song_obj, artist_wikidata_id, artist_name):
    existing_instanceOf_ids = get_wikidata_property_values(entity, INSTANCE_OF_ID)

    data = entity.statements
    song_mb_id = get_musicbrainz_song_id(song_obj)
    # Set to be musician if not already 
    if SONG_ID not in existing_instanceOf_ids:
        # Add occupation musician relation
        data.append(wdi_core.WDItemID(value=SONG_ID, prop_nr=INSTANCE_OF_ID))
    # Set MusicBrainzID if not already set 
    if MUSIC_BRAINZ_SONG_PROP_ID not in entity.wd_json_representation['claims']:
        data.append(wdi_core.WDExternalID(value=get_musicbrainz_song_id(song_obj), prop_nr=MUSIC_BRAINZ_SONG_PROP_ID))   
    elif song_mb_id not in get_wikidata_property_values(entity, MUSIC_BRAINZ_SONG_PROP_ID):
        data.append(wdi_core.WDExternalID(value=get_musicbrainz_song_id(song_obj), prop_nr=MUSIC_BRAINZ_SONG_PROP_ID))   
    # Set performer to be the artist if no performer set or performer is not artist
    if PERFORMER_ID not in entity.wd_json_representation['claims']:
        data.append(wdi_core.WDItemID(value=artist_wikidata_id, prop_nr=PERFORMER_ID))
    elif artist_wikidata_id not in get_wikidata_property_values(entity, PERFORMER_ID):
        data.append(wdi_core.WDItemID(value=artist_wikidata_id, prop_nr=PERFORMER_ID))
    

    entity.set_description(f"Song performed by {artist_name}")

    write_to_wikidata(entity, data)
    print(f"Song {get_song_name(song_obj)} by {artist_name} has been created on WikiData server.")

def create_song(song_obj, artist_wikidata_id, artist_name):
    data = []
    song_name = get_song_name(song_obj)
    data.append(wdi_core.WDItemID(value=SONG_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=artist_wikidata_id, prop_nr=PERFORMER_ID))
    data.append(wdi_core.WDExternalID(value=get_musicbrainz_song_id(song_obj), prop_nr=MUSIC_BRAINZ_SONG_PROP_ID))


    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(song_name)
    entity.set_description(f"Song by {artist_name}")
    
    
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Song {song_name} by {artist_name} has been created on WikiData server.")

def update_or_create_song(song_obj, artist_wikidata_id, artist_name):
    song_name = get_song_name(song_obj)
    entity = retrieve_song_from_wikidata_if_exists(song_name, artist_wikidata_id)
    if entity:
        update_song(entity, song_obj, artist_wikidata_id, artist_name)
    else: 
        create_song(song_obj, artist_wikidata_id, artist_name)

def remove_artist_instance(artist_name):
    search_results = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
    existing_class_ids = get_wikidata_property_values(entity, INSTANCE_OF_ID)
    if MUSICIAN_ID in existing_class_ids:
        data = [] 
        # Keep existing instaceOf relations 
        existing_class_ids.remove(MUSICIAN_ID) 
        for class_id in existing_class_ids:
            data.append(wdi_core.WDItemID(value=class_id, prop_nr=INSTANCE_OF_ID))
        write_to_wikidata(entity, data)

def remove_musicbrainzid_instance(artist_name):
    search_results = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
    property_ids = get_property_ids(entity)
    if MUSIC_BRAINZ_PROP_ID in existing_class_ids:
        data = [] 
        # Keep existing instaceOf relations 
        property_ids.remove(MUSIC_BRAINZ_PROP_ID) 
        for class_id in existing_class_ids:
            data.append(wdi_core.WDItemID(value=class_id, prop_nr=INSTANCE_OF_ID))
        write_to_wikidata(entity, data)
        
        