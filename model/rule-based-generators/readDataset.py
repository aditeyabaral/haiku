import os
import json

with open("../../data/dataset.json") as d:
    data = json.load(d)

print(len(data),type(data)) # 7 <class 'list'>