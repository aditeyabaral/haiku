import tracery
import string
import nltk
import spacy
import random

nlp = spacy.load('en_core_web_sm')

text = '''When I say that I’m an experimental computer poet, what I mean is that I write computer programs that write poems. Part of what I want to do in this talk is offer a new framework for thinking about what it means to write computer programs that write poems. Because usually when we think about computer generated poetry, we think of articles like this where any instance of some human task being automated is met by some story that’s like, “I welcome our robotic X overlords” where I replace X with whatever task is being automated by a computer. Most people when they think of computer poetry think that the task of the computer poet is to recreate with as much fidelity as possible poetry that is written by humans. I have no interest in making poetry that looks like it was written by humans. I think that that’s a plainly boring task that nobody should try to attempt.'''


def is_plural(word):
    # Special case this since one comes up a lot
    if word['text'] == 'men' or word['text'] == 'women':
        return True
    return word['text'][-1] == 's'


def is_plural_verb(word):
    if word['text'] == 'have':
        return True
    return word['text'][-1] != 's'


def is_present(word):
    return word['text'][-1] == 's'


def starts_with_vowel(word):
    vowels = set(['a', 'e', 'i', 'o', 'u'])
    return word['text'][0] in vowels


def parse_words(text):
    words = [{"text": w.translate(str.maketrans(
        {a: None for a in string.punctuation}))} for w in nltk.tokenize.word_tokenize(text)]
    # for box in boxes:
    #    word = box.content.strip()
    #    word = word.translate(str.maketrans(
    #        {a: None for a in string.punctuation}))
    #    words.append({'text': word, 'box': box})
    #sent = ' '.join([w['box'].content for w in words])
    doc = nlp(text)
    for token in doc:
        for word in words:
            text = word['text']
            if token.text == text:
                word['token'] = token
                word['pos'] = token.pos_
    return words


def find_boxes_for_grammar(words):
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

    for pos in grammar:
        while True:
            word = words[word_index]
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

            if 'pos' in word and word['pos'] == pos and pick_this and random.randint(0, 30) == 0:
                #print("Picking ", word['text'], " ", word['token'].dep_)
                picks.append(word)
                prev_pos = pos
                word_index += 1
                break
            print(picks)

            word_index += 1
    return picks


words = parse_words(text)
print(words)
grammar = find_boxes_for_grammar(words)
print(grammar)
