#!/usr/bin/env python

from string import punctuation
import random
import os


def response():
    with open(os.path.abspath('') + '/lib/steele1983.txt') as f:
        text = f.read()
    text = [i.strip(punctuation) for i in text.lower().split() if i.isalpha()]
    markov = {}
    sentence_length = random.randint(15, 20)
    for (w1, w2) in zip(text[:-1], text[1:]):
        markov.setdefault(w1, []).append(w2)
    seed = random.choice(text)
    sentence = [seed]
    for i in range(sentence_length):
        sentence.append(random.choice(markov[sentence[-1]]))
    return ' '.join(sentence)
