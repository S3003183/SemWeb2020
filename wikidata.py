from wikidataintegrator import wdi_core, wdi_login

MUSICIAN_ID = 'Q639669'
INSTANCE_OF_ID = 'P31'
HUMAN_ID = 'Q5'
MUSICIAN = "Musician"
LABEL_PROP_LINK = "http://www.w3.org/2000/01/rdf-schema#label"
MUSIC_BRAINZ_PROP_LINK = 'http://purl.org/ontology/mo/musicbrainz'
MUSIC_BRAINZ_PROP_ID = 'P434'

def get_instanceOf_ids(entity):
    ids = []
    for i in entity.wd_json_representation['claims'][INSTANCE_OF_ID]:
        ids.append(i['mainsnak']['datavalue']['value']['id'])

    return ids

def get_property_ids(entity):
    return entity.wd_json_representation['claims']

def write_to_wikidata(entity, data):
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.update(data)
    entity.write(login_instance)
    

def update_artist(entity, artist_obj):
    existing_class_ids = get_instanceOf_ids(entity)
    data = [] 
    # Keep existing instaceOf relations  
    for class_id in existing_class_ids:
        data.append(wdi_core.WDItemID(value=class_id, prop_nr=INSTANCE_OF_ID))
    # Set to be musician if not already 
    if MUSICIAN_ID not in existing_class_ids:
        # Add instanceOf musician relation
        data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
    # Set MusicBrainzID if not already set 
    if MUSIC_BRAINZ_PROP_ID not in existing_class_ids:
        # Add MusicBrainzID relation
        data.append(wdi_core.WDExternalID(value=get_musicbraiz_id(artist_obj), prop_nr=MUSIC_BRAINZ_PROP_ID))
    
    write_to_wikidata(entity, data)
    print(f"Entity {get_artist_name(artist_obj)} has been updated.")

def create_artist(artist_obj):
    data = []
    artist_name = get_artist_name(artist_obj)
    data.append(wdi_core.WDItemID(value=HUMAN_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(artist_name)
    entity.set_description(MUSICIAN)
    data.append(wdi_core.WDExternalID(value=get_musicbraiz_id(artist_obj), prop_nr=MUSIC_BRAINZ_PROP_ID))
    
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Entity {artist_name} has been created.")

def get_attribute(artist_obj, attribute_link):
    for data_prop in artist_obj:
        if data_prop['property']['value'] == attribute_link:
            attr_value=data_prop['hasValue']['value']
            return attr_value

def get_artist_name(artist_obj):
    return get_attribute(artist_obj, LABEL_PROP_LINK)

def get_musicbraiz_link(artist_obj):
    return get_attribute(artist_obj, MUSIC_BRAINZ_PROP_LINK)

def get_musicbraiz_id(artist_obj):
    result = get_musicbraiz_link(artist_obj)
    result = result.replace('http://musicbrainz.org/artist/', '')
    return result

# def get_musicbraiz_id(artist_obj):
    

def update_or_create_artist(artist_obj):
    artist_name = get_artist_name(artist_obj)
    search_results = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    if len(search_results) > 0:
        entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
        update_artist(entity, artist_obj)
    else: 
        create_artist(artist_obj)

def remove_artist_instance(artist_name):
    search_results = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
    existing_class_ids = get_instanceOf_ids(entity)
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
        
        