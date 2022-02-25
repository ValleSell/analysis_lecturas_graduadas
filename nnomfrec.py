import os
import spacy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', required=True)
parser.add_argument('--people_terms', required=True)

args = parser.parse_args()

nlp = spacy.load("es_core_news_md")

path_in= args.input_dir
filelist = os.listdir(path_in)
lnn=[]
nnfrec=[]
for i in filelist:
     if i.endswith(".txt"):
        with open(path_in + i, 'r', encoding="UTF8") as file:
            doc=nlp(file.read())
            chunki=doc.noun_chunks
            for np in chunki:
                lnn.append(np)
print ("lnn:")
print (lnn)

onlytext=[]
for nn in lnn:
    onlytext.append(nn.text.lower())
print (len(lnn))
print (len(onlytext))
print ("onlytext:")
print (onlytext)


second=[]
for e in onlytext:
    s=e.split(" ")
    if len(s)>1:
        second.append(s[1])
print (len(second))
print (second)

morethan=[]
for nn in second:
    if (second.count(nn))>10:
        morethan.append(nn)
print (len(morethan))
print (morethan)

noreps=[]
[noreps.append(nn) for nn in morethan if nn not in noreps]
print (len(noreps))
print ("noreps:")
print (noreps)

l=[]
with open(args.people_terms, 'r', encoding="utf-8") as infile:
    for line in infile:
        e = (line.strip().split(','))[0]
        l.append(e)
#print ("l:")
#print (l)

compara=[]
for e in noreps:
    if e not in l:
        compara.append(e)
#longitud de la lista de núcleos nominales no incluidos en el archivo csv
print ("compara:")
print (len(compara))
print (compara)
