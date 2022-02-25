import os
import googletrans
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', required=True)
parser.add_argument('--output_dir', required=True)

args = parser.parse_args()

#para trabajar con la API de googletrans
from googletrans import Translator
traductor= Translator()

#get the list from previously generated file gender_terms
with open(os.path.join(args.input_dir, "gender_terms.csv"), "r", encoding="utf-8") as f:
    file = f.readlines()
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "terminos_genero.csv"), "a", encoding="utf-8") as g:
#        n=0
        for line in file:
#            n += 1
#            if n == 75:
#                time.sleep(180)
#                print ("--awake--")
#                n = 0
            linea=line.split(",")
            traduc = traductor.translate(linea[0], src="auto", dest="es").text
            print (traduc)
            g.write(traduc +"," + linea[1] + "," + linea[2])


