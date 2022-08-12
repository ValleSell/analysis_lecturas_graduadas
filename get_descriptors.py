# adaptation from get_descriptors.py from Dora Demszky and Lui Lucy
# it identifies verbs and adjectives used with all terms included in the two defined groups (male and female)

import argparse
from helpers import *
import spacy_stanza
nlp = spacy_stanza.load_pipeline("es")

import os
import math

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', required=True)
parser.add_argument('--output_dir', required=True)
parser.add_argument('--gender_terms', required=True)

args = parser.parse_args()

nombres_signif=["cándido", "vega", "vera", "victoria", "diana", "jacinto", "modesto", "león", "nacho", "iria", "urbano", "ángel", "clemente", "estrella", "magdalena", "augurio", "lucía", "flora", "escarlata", "luz", "gracia", "paz", "gloria", "felicidad", "mia", "marina", "dolores", "concepción", "estela", "alma", "bonita", "rosa", "azucena", "consuelo", "pilar", "urraca"]

def run_depparse(possible_marks, word2dem,
                 book_lines, title, nlp):
    '''
    Get adjectives and verbs used with words included in the two defined groups (male and female).
    @inputs:
    - possible_marks: like "chica"
    - word2dem: word to demographic category, associates "chica" to "women"
    - book_lines: strings of textbook content in a list
    - title: title of graded reader
    - outfile: opened file
    - nlp: stanza from Stanford University pipeline

    '''
    print("Running dependency parsing for", title)
    # Break up every textbook into 5k line chunks to avoid spaCy's text length limit, maybe unnecessary with stanza...
    j = 0
    k = 0
    num_lines = len(book_lines)
    res = []
    for i in range(0, num_lines, 5000):
        chunk = '\n'.join(book_lines[i:i + 5000])
        doc = nlp(chunk)
        k += 1
        print("Finished part", k, "of", math.ceil(num_lines/5000))
        prev_word = None
        prev_word_pos = None
        for token in doc:
            j += 1
            word = token.text.lower()
            lemma = token.lemma_
            target_term = token.head.text.lower()
            target_lemma=token.head.lemma_
            if len(word2dem[word]) > 0:
                if token.pos_ != 'PROPN' and \
                    token.pos_ != 'NOUN' and token.pos_ != 'PRON':
                    prev_word=word
                    prev_word_pos=token.pos_
                    continue
                if word in possible_marks:
                    if word in nombres_signif:
                        if not token.text.istitle():
                            prev_word = word
                            prev_word_pos = token.pos_
                            continue
                        else:
                            dem = word2dem[word]
                    else:
                        dem = word2dem[word]
                if word not in possible_marks:
                    # check previous word
                    if prev_word in possible_marks and prev_word_pos == "DET":
                        # dem_dict[word2dem[word]] += 1
                        dem = word2dem[prev_word]
                        # check if previous word  is an adjective ended in -a, e.g. "famosa detective"
                    elif prev_word_pos == "ADJ":
                        if prev_word[-1] == "a" or prev_word[-2:] == "as":
                            dem = word2dem["mujer"]
                        # check if it ends in -o or -os
                        elif prev_word[-1] == "o" or prev_word[-2:] == "os":
                            dem = word2dem["hombre"]


                if token.dep_ == 'nsubj' and (token.head.pos_ == 'VERB' or token.head.pos_ == 'ADJ'):
                    res.append((str(j), title, word, dem, target_lemma, token.head.pos_, token.dep_))

                #important: it does NOT correctly work with Spanish passive voice!
                if token.dep_ == 'nsubjpass' and token.head.pos_ == 'VERB':
                    res.append((str(j), title, word, dem, target_lemma, token.head.pos_, token.dep_))
                    if prev_word in possible_marks and word in possible_marks:
                        other_dem = set(word2dem[prev_word]) - set(dem)
                        if len(other_dem) > 0:
                            res.append((str(j), title, prev_word, other_dem, target_lemma,
                                token.head.pos_, token.dep_))
                if (token.dep_ == 'obj' or token.dep_ == 'dobj') and token.head.pos_ == 'VERB':
                    res.append((str(j), title, word, dem, target_lemma, token.head.pos_, token.dep_))
                    if prev_word in possible_marks and word in possible_marks:
                        other_dem = set(word2dem[prev_word]) - set(dem)
                        if len(other_dem) > 0:
                            res.append((str(j), title, prev_word, other_dem, target_lemma,
                                token.head.pos_, token.dep_))


            if token.dep_ == 'amod':
                if len(word2dem[target_lemma]) > 0:
                    if token.head.pos_ != 'PROPN' and \
                    token.head.pos_ != 'NOUN' and token.head.pos_ != 'PRON':
                        prev_word = word
                        prev_word_pos = token.pos_
                        continue
                    if target_lemma in nombres_signif:
                        if not token.text.istitle():
                            prev_word = word
                            prev_word_pos = token.pos_
                            continue
                        else:
                            dem = word2dem[target_term]
                    else:
                        dem = word2dem[target_term]
                    prev_target_term = 'xxxxxx'
                    prev_index = token.head.i - 1
                    if prev_index >= 0:
                        prev_target_term = doc[prev_index].text.lower()
                    if prev_target_term in possible_marks and target_term not in possible_marks:
                        # term is marked, assign to marker's category
                        dem = word2dem[prev_target_term]
                    elif word[-1] == "a" or word[-2:] == "as":
                        dem = word2dem["mujer"]
                        # comprobar si termina en -o o en -os
                    elif word[-1] == "o" or word[-2:] == "os":
                        dem = word2dem["hombre"]
                    res.append((str(j), title, target_term, dem, lemma, token.pos_, token.dep_))


            prev_word = word
            prev_word_pos = token.pos_


    return res

def main():
    possible_marks, not_marks = split_terms_into_sets(args.gender_terms)
    word2dem = get_word_to_category(args.gender_terms)

    # load stanza
    nlp = spacy_stanza.load_pipeline("es")
    books = get_book_txts(args.input_dir, splitlines=True)
    outfile = codecs.open(os.path.join(args.output_dir, 'descripc_stanza_wo_lo_new.csv'), 'w', encoding='utf-8')
    for title, textbook_lines in books.items():
        res = run_depparse(possible_marks, word2dem,
            textbook_lines, title, nlp)

        for tup in res:
            if type(tup[3]) == list or type(tup[3]) == set:
                for d in tup[3]:
                    outfile.write(tup[0] + ',' + tup[1] + ',' + tup[2] + ',' + d + ',' + \
                                    tup[4] + ',' + tup[5] + ',' + tup[6] + '\n')
            else:
                outfile.write(tup[0] + ',' + tup[1] + ',' + tup[2] + ',' + tup[3] + ',' + \
                                    tup[4] + ',' + tup[5] + ',' + tup[6] + '\n')
    outfile.close()

if __name__ == '__main__':
    main()