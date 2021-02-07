#!/usr/bin/python3

import os
import random
from statistics import mean
import string
import uuid
import sys, getopt

import tracery
import spacy
import csv

nlp = spacy.load('en')

def parse_words(poem):
    word_list = []
    for word in poem.split():
        word = word.translate(str.maketrans({a:None for a in string.punctuation})).replace("\n", " ")
        word_info = {}
        word_info["text"] = word
        # print(word_info)
        word_list.append(word_info)

    sent = ' '.join([w["text"] for w in word_list])
    # print("sent", sent)
    doc = nlp(sent)
    for token in doc:
        # print("token:", token)
        for word in word_list:
            text = word['text']
            if token.text == text:
                word['token'] = token
                word['pos'] = token.pos_
    return word_list

def is_plural(word):
    if len(word['text'])==0:
        return False
    if word['text'] == 'men' or word['text'] == 'women':  # Special case this since one comes up a lot
        return True
    return word['text'][-1] == 's'

def is_plural_verb(word):
    if len(word['text'])==0:
        return False
    if word['text'] == 'have':
        return True
    return word['text'][-1] != 's'

def is_present(word):
    if len(word['text'])==0:
        return False
    return word['text'][-1] == 's'

def starts_with_vowel(word):
    vowels = set(['a', 'e', 'i', 'o', 'u'])
    if len(word['text'])==0:
        return False
    return word['text'][0] in vowels

def find_boxes_for_grammar(boxes):
    words = parse_words(boxes)
    # print('parse output', words, '\n')
    # print(len(words))
    grammars = [
        ['DET', 'NOUN', 'VERB', 'NOUN'],
        ['ADJ', 'NOUN', 'VERB', 'NOUN'],
        ['ADJ', 'NOUN', 'VERB', 'ADV'],
        ['DET', 'NOUN', 'VERB', 'NOUN', 'CONJ', 'NOUN'],
        ['VERB', 'DET', 'NOUN'],
        ['ADV', 'VERB', 'NOUN', 'CONJ', 'NOUN']
    ]
    grammar = random.choice(grammars)
    picks = []
    word_index = 0
    prev_word = None
    prev_pos = None
    length = len(words)
    n = 0
    for pos in grammar:
        while n<length:
            n+=1
            word = words[word_index]
            # print("word", word)
            # break
            if len(picks) > 0:
                prev_word = picks[-1]
                prev_pos = prev_word['pos']
            pick_this = True
            if prev_pos == 'DET':
                if prev_word['text'] == 'a' or prev_word['text'] == 'an':
                    # Pick this if it's singular
                    pick_this = not is_plural(word)
                if prev_word['text'] == 'a':
                    # Pick this if it doesn't start with a vowel
                    pick_this = not starts_with_vowel(word) and pick_this
                if prev_word['text'] == 'an':
                    pick_this = starts_with_vowel(word) and pick_this
                if prev_word['text'] == 'this':
                    pick_this = not is_plural(word) and pick_this
                if prev_word['text'] == 'these':
                    pick_this = is_plural(word) and pick_this
            if prev_pos == 'NOUN':
                # If the previous noun was plural, the verb must be plural
                if is_plural(prev_word):
                    pick_this = is_plural_verb(word) and pick_this
                if not is_plural(prev_word):
                    pick_this = not is_plural_verb(word) and pick_this
            if prev_pos == 'VERB':
                # If the verb was plural, the noun must be
                if is_plural_verb(prev_word):
                    pick_this = is_plural(word) and pick_this
                if not is_plural_verb(prev_word):
                    pick_this = not is_plural(word) and pick_this
            if pos == 'VERB':
                # Don't pick auxilliary verbs as they won't have a helper
                if 'token' in word:
                    pick_this = word['token'].dep_ != 'aux' and pick_this

            if 'pos' in word and word['pos'] == pos and pick_this:
                #print("Picking ", word['text'], " ", word['token'].dep_)
                picks.append(word)
                prev_pos = pos
                word_index += 1
                break

            word_index += 1
    return [p['text'] for p in picks]

def main(argv):

    try:
        inputfile = argv[1]
        outputfile = argv[2]
        g = open(inputfile,"r")
        inp = g.read()
        g.close()

    except:
        print("Create a input text file")
        print("Usage : python haiku_generator.py in.txt out.txt")
        sys.exit(1)


    unique_haiku = []
    for i in range(20):
        out = ' '.join(find_boxes_for_grammar(inp)).strip().lower()
        if out not in unique_haiku:
            # print("Haiku = ", out)
            unique_haiku.append(out)

    f = open(outputfile,"w")
    f.write(str(unique_haiku))
    f.close()
    print("Output Generated")



if __name__ == "__main__":
    main(sys.argv)
    