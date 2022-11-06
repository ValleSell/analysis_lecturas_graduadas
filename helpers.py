#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: Dora Demszky (ddemszky@stanford.edu) and Lucy Li (lucy3_li@berkeley.edu)
import codecs
import glob
import string
import nltk
import re
from gensim.models import KeyedVectors
import seaborn as sns
from collections import defaultdict

stopwords = open("wordlists/stopwords/es/ES_stopwords.txt", "r").read().splitlines()
punct_chars = list((set(string.punctuation) | {'»', '–', '—', '-',"­", '\xad', '-', '◾', '®', '©','✓','▲', '◄','▼','►', '~', '|', '“', '”', '…', "'", "`", '•', '*', '■'} - {"'"}))
punct_chars.sort()
punctuation = ''.join(punct_chars)
replace = re.compile('[%s]' % re.escape(punctuation))
sno = nltk.stem.SnowballStemmer('spanish')
printable = set(string.printable)

def split_terms_into_sets(people_terms_path):
    '''
    If the third column of the input file is "unmarked" then the word is unmarked
    '''
    possible_marks = set()
    not_marks = set() # everything else
    with open(people_terms_path, 'r', encoding="utf-8") as infile:
        for line in infile:
            contents = line.strip().split(',')
            if contents[2] == 'unmarked':
                not_marks.add(contents[0].lower())
            else:
                possible_marks.add(contents[0].lower())
    return possible_marks, not_marks

def get_word_to_category(people_terms_path):
    '''
    word2dem = {'madre':['mujeres'], 'tío': ['hombres']}
    '''
    word2dem = defaultdict(list)
    with open(people_terms_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            contents = line.strip().split(',')
            word2dem[contents[0]].append(contents[1])
    return word2dem

def clean_text(text,
               remove_stopwords=True,
               remove_numeric=True,
               stem=False,
               remove_short=True):
    # lower case
    text = text.lower()
    # eliminate urls
    text = re.sub(r'http\S*|\S*\.com\S*|\S*www\S*', ' ', text)
    # substitute all other punctuation with whitespace
    text = replace.sub(' ', text)
    # replace all whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    # strip off spaces on either end
    text = text.strip()
    # make sure all chars are printable
    text = ''.join([c for c in text if c in printable])
    words = text.split()
    if remove_stopwords:
        words = [w for w in words if w not in stopwords]
    if remove_numeric:
        words = [w for w in words if not w.isdigit()]
    if stem:
        words = [sno.stem(w) for w in words]
    if remove_short:
        words = [w for w in words if len(w) >= 3]
    return words

def get_book_txts(path, splitlines=False):
    print('Getting books...')
    bookfiles = sorted([f for f in glob.glob(path + '\\*.txt')])
    books = {}
    for f in bookfiles:
        txt = codecs.open(f, 'r', encoding='utf-8').read()
        if splitlines:
            txt = txt.splitlines()
        title = f.split('\\')[-1].split(".")[0]
        books[title] = txt
        print(title)
    print("Finished getting books.")
    return books

def get_models(filelist):
    model_files = [f for f in filelist if f.endswith('.wv')]
    models = [KeyedVectors.load(fname, mmap='r') for fname in model_files]
    return models

