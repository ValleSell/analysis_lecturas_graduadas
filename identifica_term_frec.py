#based on the script count_mentions from Dora Demszky and Li Lucy from this repository
#este script realiza un cómputo de todos los términos utilizados para referirse
# a los grupos (hombres y mujeres) de la lista people_terms


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


def main():
    possible_marks, not_marks = split_terms_into_sets(args.people_terms)
    word2dem = get_word_to_category(args.people_terms)

    # load spacy
    nlp = spacy.load("es_core_news_md")

    # load books
    books = get_book_txts(args.input_dir, splitlines=True)

    print('Counting groups of people...')
    os.makedirs(args.output_dir, exist_ok=True)
    listado=[]
    frecM={}
    frecH={}
    with codecs.open(os.path.join(args.output_dir, "term_frecuentes_nuevas.json"), 'a', encoding='utf-8') as f:
        for title, book_lines in books.items():
            print(title)
            dem_dict = Counter() # demographic : count
            for line in book_lines:
                doc = nlp(line)
                prev_word = None
                for token in doc:
                    word = token.text.lower()
                    # filtrar palabras que no sean sustantivos, nombres propios ni pronombres
                    if token.pos_ != 'PROPN' and \
                        token.pos_ != 'NOUN' and token.pos_ != 'PRON':
                        prev_word = word
                        prev_word_pos = token.pos_
                        continue
                    if word in possible_marks:
                        #añade la palabra al listado como masc o fem
                        listado.append((word,word2dem[word]))

                        # sustantivos como "detective" o "periodista" son iguales en fem y masc
                    elif word in not_marks:
                        # comprobar si palabra anterior esta marcada como masc o fem, ej. "una"
                        if prev_word in possible_marks and prev_word_pos == "DET":
                            listado.append(word)
                        # comprobar si palabra ant es adj. terminado en -a, ej. "famosa detective"
                        elif prev_word_pos == "ADJ":
                            if prev_word[-1] == "a" or prev_word[-2:] == "as":
                                listado.append((word, "mujeres"))
                            # en caso contrario contar como masc
                                # comprobar si termina en -o o en -os
                            elif prev_word[-1] == "o" or prev_word[-2:] == "os":
                                listado.append((word, "hombres"))
                    prev_word = word
                    prev_word_pos = token.pos_



        for i in listado:
            if i[1]=="mujeres" or i[1]==['mujeres']:
                if i[0] not in frecM:
                    frecM[i[0]]=1
                else:
                    frecM[i[0]]+=1
            if i[1] =="hombres" or i[1]==['hombres']:
                if i[0] not in frecH:
                    frecH[i[0]]=1
                else:
                    frecH[i[0]]+=1


        f.write(str(frecM))
        f.write("<-arriba frec mujeres, abajo hombres->")
        f.write(str(frecH))
#            for demographic in dem_dict:
#                f.write(title + ',' + demographic + ',' + str(dem_dict[demographic]) + '\n')
#               f.write(str(listado))

if __name__ == '__main__':
    main()