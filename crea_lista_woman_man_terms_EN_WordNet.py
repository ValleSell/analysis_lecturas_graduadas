import nltk
from nltk.corpus import wordnet as wn

import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output_dir', required=True)
args = parser.parse_args()

def busca_hipos (var):
    #la función puede partir de una palabra o una lista (var), busca en WordNet
    #y crea una lista que inlcuye la palabra o la lista de palabras inicial más todos
    #los hipónimos de esta incluidos en WordNet
    if type(var)==str:
        #en este caso la variable es una palabra (un string, str)
        wns=wn.synsets(var)
        gen_words=[lemma.name() for synset in wns for lemma in synset.lemmas() if synset._lexname=="noun.person"]
        terms=[]
        # borra nombres_signif , ' y duplicados
        [terms.append((e.replace("nombres_signif", " ")).replace("`", "")) for e in gen_words if e not in terms]
        return terms
    elif type (var)==list:
        #en este caso la variable es una lista (list)
        for e in var:
            sys=wn.synsets(e)
            for sy in sys:
                if sy._lexname=="noun.person":
                    hy=sy.hyponyms()
                    lista=[lemma.name() for synset in hy for lemma in synset.lemmas()]
                    var=var+lista
    terms=[]
    [terms.append((e.replace("nombres_signif", " ")).replace("`", "")) for e in var if e not in terms]
    return terms


#tb=término a buscar
tb="woman"
#n=número de iteraciones
n=4
women_words= busca_hipos (tb)
for e in range (n):
    women_words= busca_hipos (women_words)


#escribe un archivo con los resultados
os.makedirs(args.output_dir, exist_ok=True)
with open(os.path.join(args.output_dir, "gender_terms.csv"), "a", encoding="utf-8") as f:
    for e in women_words:
        f.write(e + ",women,gender" + '\n')

#repetir para hombres
tb="man"
n=4
men_words= busca_hipos (tb)
for e in range (n):
    men_words= busca_hipos (men_words)

os.makedirs(args.output_dir, exist_ok=True)
with open(os.path.join(args.output_dir, "gender_terms.csv"), "a", encoding="utf-8") as f:
    for e in men_words:
        f.write(e + ",men,gender" + '\n')