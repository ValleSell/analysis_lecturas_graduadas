import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', required=True)


args = parser.parse_args()

l=[]
n=0
with open(args.input_dir, 'r', encoding='utf-8') as f:
    for linea in f:
        n+=1
        pal= linea.split(" ")[0]
        if pal[0].isupper():
            l.append(pal)
print ("El " , str((len(l)/n)*100) , "% de las entradas de la lista son érroneas")

