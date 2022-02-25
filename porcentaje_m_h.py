#este script calcula los porcentajes de menciones en:
# - el total de las lecturas
# - las lecturas con personajes principales femeninos
# - las lecturas con personajes principales masculinos
# - las lecturas con personajes principales de los dos sexos



import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input_file', required=True)

args = parser.parse_args()

#cálculo del porcentaje total
h=0
m=0
with open(args.input_file, 'r', encoding="UTF8") as infile:
    for line in infile.readlines():
        linea=line.split(",")
#        print(linea[0], str(int(linea[2])/(int(linea[2])+int(linea[-1]))), "% hombres, ", str(int(linea[-1])/(int(linea[2])+int(linea[-1]))), "% mujeres")
        h+=int(linea[2])/(int(linea[2])+int(linea[-1]))
        m+=int(linea[-1])/(int(linea[2])+int(linea[-1]))
print ("porcentaje hombres:")
ph=h/47
print (ph)
print ("porcentaje mujeres:")
pm=m/47
print (pm)

#cálculo en las lecturas con protagonistas femeninos
h_m=0
m_m=0
num_m=0
with open(args.input_file, 'r', encoding="UTF8") as infile:
    for line in infile.readlines():
        linea=line.split(",")
        if (linea[0].split("_"))[3]=="M":
            num_m+=1
            h_m+=int(linea[2])/(int(linea[2])+int(linea[-1]))
            m_m+=int(linea[-1])/(int(linea[2])+int(linea[-1]))
print (num_m)
print ("porcentaje hombres lecturas prota fem:")
ph_m=h_m/num_m
print (ph_m)
print ("porcentaje mujeres lecturas prota fem:")
pm_m=m_m/num_m
print (pm_m)

#cálculo en las lecturas con protagonistas masculinos
h_h=0
m_h=0
num_h=0
with open(args.input_file, 'r', encoding="UTF8") as infile:
    for line in infile.readlines():
        linea=line.split(",")
        if (linea[0].split("_"))[3]=="H":
            num_h+=1
            h_h+=int(linea[2])/(int(linea[2])+int(linea[-1]))
            m_h+=int(linea[-1])/(int(linea[2])+int(linea[-1]))
print (num_h)
print ("porcentaje hombres lecturas prota masc:")
ph_h=h_h/num_h
print (ph_h)
print ("porcentaje mujeres lecturas prota masc:")
pm_h=m_h/num_h
print (pm_h)


#cálculo en las lecturas con protagonistas de los dos sexos
h_mh=0
m_mh=0
num_mh=0
with open(args.input_file, 'r', encoding="UTF8") as infile:
    for line in infile.readlines():
        linea=line.split(",")
        if (linea[0].split("_"))[3]=="MH":
            num_mh+=1
            h_mh+=int(linea[2])/(int(linea[2])+int(linea[-1]))
            m_mh+=int(linea[-1])/(int(linea[2])+int(linea[-1]))
print (num_mh)
print ("porcentaje hombres lecturas protas mixtos:")
ph_mh=h_mh/num_mh
print (ph_mh)
print ("porcentaje mujeres lecturas protas mixtos:")
pm_mh=m_mh/num_mh
print (pm_mh)

j=num_mh+num_h+num_m
print (j)