#adaptación de count_mentions.py de Dora Demszky y Lui Lucy
#calcula el número de veces que se nombra a individuos de un grupo u otro, en mi caso, hombres y mujeres

import spacy
from helpers import *
import argparse
import os
import codecs
from collections import Counter

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', required=True)
parser.add_argument('--output_dir', required=True)
parser.add_argument('--people_terms', required=True)

args = parser.parse_args()

nombres_signif=["cándido", "vega", "vera", "victoria", "diana", "jacinto", "modesto", "leon", "nacho", "iria", "urbano", "ángel", "clemente", "estrella", "magdalena", "lucía", "flora", "escarlata", "luz", "gracia", "paz", "gloria", "felicidad", "mia", "marina", "dolores", "concepción", "estela", "alma", "bonita", "rosa", "azucena", "consuelo", "pilar", "urraca"]

def update_dict(dem_dict, word2dem, word):
    for cat in word2dem[word]:
        dem_dict[cat] += 1
    return dem_dict

def main():
    possible_marks, not_marks = split_terms_into_sets(args.people_terms)
    word2dem = get_word_to_category(args.people_terms)

    # load spacy
    nlp = spacy.load("es_core_news_md")

    # load books
    books = get_book_txts(args.input_dir, splitlines=True)

    print('Counting groups of people...')
    os.makedirs(args.output_dir, exist_ok=True)
    with codecs.open(os.path.join(args.output_dir, "menciones_hom_muj.csv"), 'w', encoding='utf-8') as f:
        for title, book_lines in books.items():
            print(title)
            dem_dict = Counter() # demographic : count
            for line in book_lines:
                doc = nlp(line)
                prev_word = None
                prev_word_pos=None
                for token in doc:
                    word = token.text.lower()
                    #filtrar palabras que no sean sustantivos, nombres propios ni pronombres
                    if token.pos_ != 'PROPN' and \
                        token.pos_ != 'NOUN' and token.pos_ != 'PRON':
                        prev_word = word
                        prev_word_pos = token.pos_
                        continue
                    #excepción pensada para casos como "José María"
                    if token.pos_ == 'PROPN' and prev_word_pos=='PROPN':
                        prev_word = word
                        prev_word_pos = token.pos_
                        continue

                    if word in possible_marks:
                        #para comprobar que realmente se trata de un nombre de pila, como Esperanza
                        if word in nombres_signif:
                            if token.text.istitle():
                                # dem_dict[word2dem[word]] += 1
                                update_dict(dem_dict, word2dem, word)
                            else:
                                prev_word = word
                                prev_word_pos = token.pos_
                                continue
                        else:
                            update_dict(dem_dict, word2dem, word)


                    #sustantivos como "detective" o "periodista" son iguales en fem y masc
                    elif word in not_marks:
                        #comprobar si palabra anterior esta marcada como masc o fem, ej. "una"
                        if prev_word in possible_marks and prev_word_pos == "DET":
                            #dem_dict[word2dem[word]] += 1
                            update_dict(dem_dict, word2dem, prev_word)
                        #comprobar si palabra ant es adj. terminado en -a, ej. "famosa detective"
                        elif prev_word_pos =="ADJ":
                            if prev_word[-1]=="a" or  prev_word[-2:]=="as":
                                update_dict(dem_dict, word2dem, "mujer")
                            #comprobar si termina en -o o en -os
                            elif prev_word[-1]=="o" or  prev_word[-2:]=="os":
                                update_dict(dem_dict, word2dem, "hombre")

                    prev_word = word
                    prev_word_pos = token.pos_
            f.write(title + ",hombres," + str(dem_dict["hombres"]) + ",mujeres," + str(dem_dict["mujeres"]) + "\n")


if __name__ == '__main__':
    main()