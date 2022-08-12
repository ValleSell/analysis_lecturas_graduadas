import nltk
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

import os
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('--output_dir', required=True)
args = parser.parse_args()

def busca_hipos_lista (l, lexname=None):
    result=[]
    for e in l:
        sys = wn.synsets(e)
        for sy in sys:
            hy = sy.hyponyms()
            lista = [lemma.name() for synset in hy for lemma in synset.lemmas() if lexname == None or synset._lexname == lexname]
            l=l+lista
    [result.append(e) for e in l if e not in result]
    return result


def busca_hipos_pal (var, n=1, lexname= None):
    #la función parte de una lista de palabras (var) y busca hipónimos en WordNet
    #y crea una lista que incluye la palabra inicial más todos
    #los hipónimos de esta incluidos y los hipónimos de los hipónimos en n niveles en WordNet
    if type(var)==str:
        var =[var]
    result_final=var
    result=var
    for z in range (n-1):
        result=busca_hipos_lista(result,lexname)
        [result_final.append(e) for e in result if e not in result_final]

    return result_final


#crea un listado con hipónimos de "woman" de cuatro niveles de profundidad
#incluyendo únicamente sustantivos para designar personas
women_words= busca_hipos_pal ("woman", 4, "noun.person")


#escribe un archivo con los resultados
os.makedirs(args.output_dir, exist_ok=True)
with open(os.path.join(args.output_dir, "gender_terms.csv"), "a", encoding="utf-8") as f:
    for e in women_words:
        f.write(e + ",women,gender" + '\n')

#repetir para hombres
men_words= busca_hipos_pal ("man", 4, "noun.person")


#os.makedirs(args.output_dir, exist_ok=True)
with open(os.path.join(args.output_dir, "gender_terms.csv"), "a", encoding="utf-8") as f:
    for e in men_words:
        f.write(e + ",men,gender" + '\n')
