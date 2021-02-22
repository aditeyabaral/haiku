import re
import string
import json
import sys
import pandas as pd
from pathlib import Path
import haikuGeneratorFromGrammar

file_to_convert = sys.argv[1]


def clean(text):
    # text = text.lower()
    text = text.strip()
    # pattern = re.compile(rf"[^\x00-\x7F]+")  # verify this --> add later --> check if words are in english dictionary
    # text = re.sub(pattern, "", text)
    return text


if file_to_convert == 'source1':
    df = pd.read_csv("../../data/sources/source1.csv")
    poems = df["text"].values
    poems = list(map(clean, poems))
    # print(poems)

if file_to_convert == 'source2':
    files = Path("../../data/sources/source2/").rglob("**/*")
    files = [str(f.resolve()) for f in files if f.is_file()]
    poems = list()
    for f in files:
        with open(f, encoding="utf-8") as fr:
            content = clean(fr.read())
            poems.append(content)
    print(len(poems))

elif file_to_convert == "source3":
    df = pd.read_csv("../../data/sources/source3.csv")
    poems = df["poem"].values
    poems = list(map(clean, poems))
    # print(poems)

elif file_to_convert == "source4":
    df = pd.read_csv("../../data/sources/source4.csv")
    poems = df["Poem"].values
    poems = list(map(clean, poems))
    # print(poems)


elif file_to_convert == "source5":
    df = pd.read_csv("../../data/sources/source5.csv")
    poems = df["Content"].values
    poems = list(map(clean, poems))
    # print(poems)

elif file_to_convert == "source6":
    df = pd.read_csv("../../data/sources/source6.csv",sep='\t',error_bad_lines=False, header=None)
    poems = df[" poem_content "].values
    poems = list(map(clean, poems))
    cleaned_poems = list()
    for p in poems:
        cleaned_poems.append('\n'.join(p.split("|")))
    poems = cleaned_poems
    # print(poems)

elif file_to_convert == "source8":
    pass

else:
    pass

# exit()
haikus = list()
total = len(poems)
for ctr, p in enumerate(poems[-1:]):
    print(f"{ctr+1}/{total}")
    result = haikuGeneratorFromGrammar.generateHaiku(p)
    haikus.append(result)

print(haikus)
with open(f'{sys.argv[1]}.json', 'w') as outfile:
    json.dump(haikus, outfile)

print("Data Generated")