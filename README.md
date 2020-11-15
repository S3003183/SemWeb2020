# WikiData music updater
A tool for updating WikiData with data obtained from MusicBraiz ontology. The tool updates existing WikiData artists and their songs if entites already exist on WikiData. If artists or songs do not exist on WikiData, they are added to WikiData. 

For artists the following properties are set: 
- `occupation` is set to be `musician (Q639669)`
- `MusicBrainz artist ID` is set to be the respective value (for example: 268ff35a-569f-4974-835c-fdefa7d9b229)

For songs the following properties are set: 
- `label` is set to be `<song name>`
- `description` is set to be `Song by <artist name>`
- `instance of` is set to be `song (Q7366)`
- `performer` is set to be `<artist wikidata id> (Q6867808)`
- `MusicBrainz work ID` is set to be the respective value (for example: 3f4836c7-3c98-45f5-adb7-5444e569fb78)

## Installation & running the project

```bash

git clone https://github.com/S3003183/SemWeb2020.git

cd SemWeb2020

pip3 install -r requirements.txt

python3 main.py
```

## Detailed description of how tool opereates

### Data collection
The tool firstly collects data from MusicBrainz ontology (accessable on [DBTune](http://dbtune.org/musicbrainz/snorql/)) via SPARQL queries. The main reason for collecting the data is issues with DBTune's availability. During the project development we experienced that the server was down multiple times each day for sereval hours. The collected data is stored 

The collected data is stored in `data` directory.
- `data/all_artists.json` stores data of all artists in the following form:
{
    {artist_name: data},
    {artist_name: data},
    ...
}
- `data/artist_allsongs/<artist_name>.json` stores data of all songs for a particular artist in the following form:
{
    {song_name: data},
    {song_name: data},
    ...
}


