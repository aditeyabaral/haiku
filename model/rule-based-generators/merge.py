import json
from os import listdir
from os.path import isfile, join

source_path = "../../data"
files = [join(source_path, f) for f in listdir(source_path) if isfile(join(source_path, f)) and ".json" in f]

data = list()
for source in files:
    with open(source) as s:
        data.append(json.load(s))

with open("../../data/dataset.json","w") as d:
    json.dump(data, d)