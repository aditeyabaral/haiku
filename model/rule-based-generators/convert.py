import os
import json
import sys
import pandas as pd
from pathlib import Path
import haikuGeneratorFromGrammar

p = Path(r'../../data/sources').glob('**/*.csv')
files = [x for x in p if x.is_file()]

file_to_convert = sys.argv[1]

if file_to_convert == 'source1':
    df = pd.read_csv("../../data/sources")
    poems = df["text"].values
    haikus = list(map(haikuGeneratorFromGrammar.generateHaiku, poems))
    print(haikus)
