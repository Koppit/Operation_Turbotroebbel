from get_studies import get_urls
import DataExtractor
import time
import json
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen

"""
urls = get_urls()
for url in urls:
    DataExtractor.extract(url)
    # vent litt mellom hver forespørsel
    time.sleep(0.5)
"""

url = "https://fagskolen-viken.no/studier/ledelse/praktisk-lederutdanning"
#DataExtractor.extract(url)

study_locations = {
}
study_types = {
}

def match_location_and_studyType(object):
    global study_locations, study_types
    object = object.split(sep=" | ") # split ut lokasjonene. Studietype splittes senere.
    study_location = {}
    study_type = {}

    new_index_locations = len(study_locations)
    new_index_types = len(study_types) 
    # Match lokasjon mot ID i databasen.
    for o in object:
        object_splitted = o.split(sep="(") # splitt ut lokasjon og studietype 
        if not study_locations: # Hvis databasen er tom, legg første lokasjon inn. 
            study_locations[0] = object_splitted[0].strip()

        for loc in range(0,4):
            target = object_splitted[0].strip()
            print(target)
            if study_locations[loc] == target:
                study_location[loc] = target
            else:
                new_index_locations += 1
                print(f"Lokasjon ikke i dict, legger til: {target} med ID {index}")
                study_locations[new_index_locations] = target
                study_location[new_index_locations] = target
        
        # Match studietype mot ID i databasen.
        for type in list(study_types.keys()):
            target = object_splitted[1].replace(")","").strip()
            
            print(f"Prøver å matche '{study_types[type]}' mot '{target}'")
            if study_types[type] == target:
                print(f"match found at type ID: {type}, adding..")
                study_type[type] = target
                #print(f"studietype: {target}, plassert som ID: {type}")
            else:
                index = loc + 1
                print("Lokasjon ikke i dict, legger til: {target} med ID {index}")
                study_types[index] = target

    return study_location, study_type


object = "Fredrikstad (Samlingsbasert 2 år) | Kjeller (Samlingsbasert 2 år) | Kongsberg (Samlingsbasert 2 år)"
study_location, study_type = match_location_and_studyType(object)

print(study_location)
print(study_type)
