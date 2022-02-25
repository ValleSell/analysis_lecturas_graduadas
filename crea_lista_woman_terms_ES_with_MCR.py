import nltk

wncr = nltk.corpus.reader.wordnet.WordNetCorpusReader("C:\\Python projects\\textbook-analysis\\MCR", None)

#https://www.nltk.org/book/ch02.html search: 5   WordNet

woman = wncr.synsets('mujer')
print (woman)
women_words = woman.hyponyms()
lista=[lemma.name() for synset in women_words for lemma in synset.lemmas()]
print("first list of hyponims of mujer")
#print(lista)
print(len(lista))
#lista_ES=lista[-34:]
lista_ES=lista

print("2nd level without English")
for l in lista_ES:
    new=wncr.synset(l + ".n.01")
    new_words=new.hyponyms()
    new_lista=[lemma.name() for synset in new_words for lemma in synset.lemmas()]
    lista_ES=lista_ES + new_lista

#print(lista_ES)
print(len(lista_ES))

print("3rd level")
for l in lista_ES:
    new=wncr.synset(l + ".n.01")
    new_words=new.hyponyms()
    new_lista=[lemma.name() for synset in new_words for lemma in synset.lemmas()]
    lista_ES=lista_ES + new_lista

#print(lista_ES)
print(len(lista_ES))

print("4th level")
for l in lista_ES:
    new=wncr.synset(l + ".n.01")
    new_words=new.hyponyms()
    new_lista=[lemma.name() for synset in new_words for lemma in synset.lemmas()]
    lista_ES=lista_ES + new_lista


print(len(lista_ES))

#lista sin nombres_signif ni `

listaSIN=[(el.replace("nombres_signif", " ")).replace ("`", "") for el in lista_ES]
print ("this is the len of listaSIN")
print (len(listaSIN))


lista_ES_no_reps=[]
for el in listaSIN:
    if el not in lista_ES_no_reps:
        lista_ES_no_reps.append(el)
print(len(lista_ES_no_reps))

women=lista_ES_no_reps

print (women)



#listadoES = []
#listado=["mujer", "tía buena", "prima", "ñalkj", "esposa", "tarara"]
#for word in listado:
#    if word in dataset:
#        listadoES.append(word)

#print (listadoES)

#from datasets import load_dataset

##all_wiki = load_dataset('large_spanish_corpus')
##all_wiki = load_dataset('large_spanish_corpus', name='all_wikis')

#dataset = load_dataset("spanish_billion_words")

#listadoES = []
#listado=["mujer", "tía buena", "prima", "ñalkj", "esposa", "tarara"]
#for word in listado:
#    if word in dataset:
#        listadoES.append(word)

#print (listadoES)

#c=0
#for dataset.text in dataset:
#   c+=1
#   print (str(dataset.text))
#   if c==100:
#       break


