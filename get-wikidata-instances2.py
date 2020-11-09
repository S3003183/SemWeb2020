from wikidataintegrator import wdi_core, wdi_login

MUSICIAN_ID = 'Q639669'
INSTANCE_OF_ID = 'P31'
LIGHTHOUSE_ID = 'Q39715'


def get_instanceOf_ids(entity):
    ids = []
    for i in entity.wd_json_representation['claims'][INSTANCE_OF_ID]:
        ids.append(i['mainsnak']['datavalue']['value']['id'])

    return ids

def get_existing_instaceOf_objects(entity):
    objects = []
    return entity.wd_json_representation['claims'][INSTANCE_OF_ID]


def main():
    search_results = wdi_core.WDItemEngine.get_wd_search_results("Jacques Loussier")
    entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
    # existing_class_ids = get_instanceOf_ids(entity)

    print(entity.wd_json_representation)
    login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')
    data = get_existing_instaceOf_objects(entity)
    newProp = wdi_core.WDItemID(value='Q21550989', prop_nr=INSTANCE_OF_ID)
    data.append(newProp)
    
    entity.update(data)
    entity.write(login_instance)
    print("Entity has been updated.")

if __name__ == "__main__":
    main()