# WikiData music updater
A tool for updating WikiData with data obtained from MusicBraiz ontology. The tool updates existing WikiData artists and songs their songs if entites already exist on WikiData. If artists or songs do not exist on WikiData, they are added to WikiData server. 

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
