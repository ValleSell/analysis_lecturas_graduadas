import json
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--app_id', required=True)
parser.add_argument('--app_key', required=True)

#wie soll ich das woanders packen??
# app_id = "8ae17dee"
# app_key = "30bfa6fe3c79037aa2d7f6236647a74d"
#
args = parser.parse_args()

endpoint = "entries" #didnt work with "words"
language_code = "es"

import time

n=0
L2=[]
for l in women:
    n+=1
    if n==50:
        n=0
        print ("sleeping...")
        time.sleep (45)
    else:
        print (n)
        word_id = l
        url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
        r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
#        print("code {}\n".format(r.status_code))
        if r.status_code !=404:
            L2.append (l)

print (L2)

print (len(L2))