
from easyocr import Reader
import os
import re

maps = os.listdir("assets/original/")
maps = [os.path.splitext(x)[0].lower() for x in maps]

macmillan = ["coal", "groaning", "suffocation", "ironworks", "shelter"]

reader = Reader(['en'], gpu=False)

def map_logic():
    map = ("", "")
    # Esegui l'OCR
    results = reader.readtext("assets/temp/screen.png", detail = 0)
        # Stampa il testo estratto

    results = [x.lower().replace(" ", "_").replace("'", "").replace("preschool_il", "preschool_ii").replace("preschool_|", "preschool_i").replace("preschool_[", "preschool_i") for x in results]
    print(results)
    print(maps)
    for i in results:
        if len(list(i.split("_"))) >= 2:
            for j in maps:
                if i in j:
                    result = re.findall('|'.join(macmillan), j)
                    print(result)
                    if len(result) >= 1:
                        map = (result[0] + "/" + result[0] + ".png", result[0] + "/" + result[0])
                    else:
                        map = (j + ".png", "")
                    return map
    if map[0] == None:
        for i in results:
            for j in maps:
                if i in j:
                    result = re.findall('|'.join(macmillan), j)
                    print(result)
                    if len(result) >= 1:
                        map = (result[0] + "/" + result[0] + ".png", result[0] + "/" + result[0])
                    else:
                        map = (j + ".png", "")
                    return map
    return map

