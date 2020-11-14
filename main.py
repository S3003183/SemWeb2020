import os
from wikidata import *
from data_collector import *
from time import sleep


######### Constants #########
ALL_ARTISTS_PATH = 'data/all_artists.json'
SONGS_DIR_PARH = 'data/songs/artist_allsongs'


######### Main program code #########
def main():
    # Collect artist and song data from DBTune MusicBrainz ontology if not collected before
    if not os.path.exists('data/artists'): 
        collect_artists_data()
    if not os.path.isfile(ALL_ARTISTS_PATH):
        combine_artist_data()
    if not os.path.exists('data/songs/artists'):
        collect_artists_songs()
    if not os.path.exists(SONGS_DIR_PARH):
        combine_song_jsons_per_artist()
    
    # Read all artists object
    all_artists = read_json(ALL_ARTISTS_PATH)

    # Get artist data
    for artist_name, artist_obj in all_artists.items():
        artist_in_path_name = artist_name.replace('/', '')
        songs = read_json(f'{SONGS_DIR_PARH}/{artist_in_path_name}.json')
        update_or_create_artist(artist_obj)
        
        # Wait for data to be updated on WikiData server
        sleep(10)
        artist_entity = retrieve_artist_from_wikidata_if_exists(artist_name)
        artist_wikidata_id = get_artist_wikidata_id(artist_entity)
        
        # Update song on WikiData server if exists. If does not exist, create a new entity on WikiData
        for song_name, song_obj in songs.items():
            update_or_create_song(song_obj, artist_wikidata_id, artist_name)

if __name__ == "__main__":
    main()

