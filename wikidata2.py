from wikidataintegrator import wdi_core, wdi_login

MUSICIAN_ID = 'Q639669'
INSTANCE_OF_ID = 'P31'
HUMAN_ID = 'Q5'
MUSICIAN = "Musician"

def get_instanceOf_ids(entity):
    ids = []
    for i in entity.wd_json_representation['claims'][INSTANCE_OF_ID]:
        ids.append(i['mainsnak']['datavalue']['value']['id'])

    return ids

def write_to_wikidata(entity, data):
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.update(data)
    entity.write(login_instance)
    

def update_artist(entity):
    existing_class_ids = get_instanceOf_ids(entity)
    if MUSICIAN_ID not in existing_class_ids:
        data = [] 
        # Keep existing instaceOf relations  
        for class_id in existing_class_ids:
            data.append(wdi_core.WDItemID(value=class_id, prop_nr=INSTANCE_OF_ID))
        # Add instanceOf musician relation
        data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
        write_to_wikidata(entity, data)
        print("Entity has been updated.")

def create_artist(artist_name):
    data = []
    data.append(wdi_core.WDItemID(value=HUMAN_ID, prop_nr=INSTANCE_OF_ID))
    data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
    entity = wdi_core.WDItemEngine(data=data)
    entity.set_label(artist_name)
    entity.set_description(MUSICIAN)
    # write_to_wikidata(entity, data)
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    entity.write(login_instance)
    print(f"Entity {artist_name} has been created.")


def update_or_create_artist(artist_name):
    search_results = wdi_core.WDItemEngine.get_wd_search_results(artist_name)
    if len(search_results) > 0:
        entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
        update_artist(entity)
    else: 
        create_artist(artist_name)

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
        