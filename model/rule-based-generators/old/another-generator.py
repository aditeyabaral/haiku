import spacy
from spacy.matcher import Matcher
import syllapy
import random

nlp = spacy.load("en_core_web_sm")
matcher2 = Matcher(nlp.vocab)
matcher3 = Matcher(nlp.vocab)
matcher4 = Matcher(nlp.vocab)

pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
           {'POS':  {"IN": ["NOUN", "VERB"]} }]
matcher2.add("TwoWords", None, pattern)
pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
           {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
           {'POS':  {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }]
matcher3.add("ThreeWords", None, pattern)
pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
           {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
           {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
           {'POS':  {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }]
matcher4.add("FourWords", None, pattern)

text = '''When I say that I’m an experimental computer poet, what I mean is that I write computer programs that write poems. Part of what I want to do in this talk is offer a new framework for thinking about what it means to write computer programs that write poems. Because usually when we think about computer generated poetry, we think of articles like this where any instance of some human task being automated is met by some story that’s like, “I welcome our robotic X overlords” where I replace X with whatever task is being automated by a computer. Most people when they think of computer poetry think that the task of the computer poet is to recreate with as much fidelity as possible poetry that is written by humans. I have no interest in making poetry that looks like it was written by humans. I think that that’s a plainly boring task that nobody should try to attempt.'''
doc = nlp(text)

matches2 = matcher2(doc)
matches3 = matcher3(doc)
matches4 = matcher4(doc)

g_5 = []
g_7 = []

for match_id, start, end in matches2 + matches3 + matches4:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span

    syl_count = 0
    for token in span:
        syl_count += syllapy.count(token.text)
    if syl_count == 5:
        if span.text not in g_5:
            g_5.append(span.text)
    if syl_count == 7:
        if span.text not in g_7:
            g_7.append(span.text)

print(g_5, g_7)

print("Enter for a new haiku. ^C to quit\n")
while (True):
    print("%s\n%s\n%s" %(random.choice(g_5),random.choice(g_7),random.choice(g_5)))
    input("\n")
