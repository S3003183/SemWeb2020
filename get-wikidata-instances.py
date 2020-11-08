from wikidataintegrator import wdi_core, wdi_login

MUSICIAN_ID = 'Q639669'
INSTANCE_OF_ID = 'P31'


def get_instanceOf_ids(entity):
    ids = []
    for i in entity.wd_json_representation['claims'][INSTANCE_OF_ID]:
        ids.append(i['mainsnak']['datavalue']['value']['id'])

    return ids


def main():
    search_results = wdi_core.WDItemEngine.get_wd_search_results("Pierre Michelot")
    entity = wdi_core.WDItemEngine(wd_item_id=search_results[0])
    existing_class_ids = get_instanceOf_ids(entity)

    if MUSICIAN_ID not in existing_class_ids:
        print("Not an instance of musician.")
        login_instance = wdi_login.WDLogin(user='SemWeb2020', pwd='nestor2020')

        data = []
        for class_id in existing_class_ids:
            data.append(wdi_core.WDItemID(value=class_id, prop_nr=INSTANCE_OF_ID))

        data.append(wdi_core.WDItemID(value=MUSICIAN_ID, prop_nr=INSTANCE_OF_ID))
        
        entity.update(data)

        entity.write(login_instance)
        print("Entity has been updated.")

if __name__ == "__main__":
    main()