from wikidataintegrator import wdi_core

MUSICIAN_ID = 'Q639669'


def get_list_of_instances(entity_name):
    item_id = wdi_core.WDItemEngine.get_wd_search_results(entity_name)
    information = wdi_core.WDItemEngine(wd_item_id=item_id[0])
    # property_list = information.get_property_list()
    list_of_instances = []

    for i in information.wd_json_representation['claims']['P31']:
        # print(i['mainsnak']['datavalue']['value']['id'])
        list_of_instances.append(i['mainsnak']['datavalue']['value']['id'])

    return list_of_instances

def main():
    pierre_michelot = get_list_of_instances("Pierre Michelot")
    if MUSICIAN_ID not in pierre_michelot:
        print("Not an instance of musician.")

if __name__ == "__main__":
    main()