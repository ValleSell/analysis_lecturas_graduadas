"""
Calculate log odds for two groups of descriptors. 
"""

import os
import json
from collections import defaultdict, Counter
import helpers
import string
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input_file', required=True)
parser.add_argument('--output_dir', required=True)
parser.add_argument('--group1', required=True)
parser.add_argument('--group2', required=True)

args = parser.parse_args()

group1 = args.group1.split(',')
group2 = args.group2.split(',')

#ellas= 'group1_counts.txt'
#ellos= 'group2_counts.txt'
#total= 'all_counts.txt'
#log='log_odds.txt'

ellas= 'group1_counts_antiguas.txt'
ellos= 'group2_counts_antiguas.txt'
total= 'all_counts_antiguas.txt'
log='log_odds_antiguas.txt'

#ellas= 'group1_counts_nuevas.txt'
#ellos= 'group2_counts_nuevas.txt'
#total= 'all_counts_nuevas.txt'
#log='log_odds_nuevas.txt'

def write_out_log_odds():
    translator = str.maketrans('', '', string.punctuation)
    marked = set() # word IDs associated with group 1
    all_count = Counter() # {(id, word) : count}
    group1_count = Counter()
    group2_count = Counter()
    with open(args.input_file, 'r', encoding="UTF8") as infile:
        for line in infile:
            contents = line.strip().split(',')
            word = contents[4]
            proc_word = word.translate(translator)
            if proc_word == '': continue
            if contents[3] in group1: 
                group1_count[proc_word] += 1
                marked.add(contents[0] + contents[1])
    # we open the file twice to avoid overlap w/ group 1
    with open(args.input_file, 'r', encoding="UTF8") as infile:
        for line in infile:
            contents = line.strip().split(',')
            word = contents[4]
            proc_word = word.translate(translator)
            if proc_word == '': continue
            if contents[3] in group2 and (contents[0] + contents[1]) not in marked: 
                group2_count[word] += 1
            all_count[word] += 1

    with open(os.path.join(args.output_dir, ellas), 'w', encoding="UTF8") as outfile:
        for word in all_count: 
            outfile.write(str(group1_count[word]) + ' ' + word + '\n')
    with open(os.path.join(args.output_dir, ellos), 'w', encoding="UTF8") as outfile:
        for word in all_count: 
            outfile.write(str(group2_count[word]) + ' ' + word + '\n')
    with open(os.path.join(args.output_dir, total), 'w', encoding="UTF8") as outfile:
        for word in all_count: 
            outfile.write(str(all_count[word]) + ' ' + word + '\n')

def descriptor_log_odds(): 
    '''
    Runs log odds on people descriptors, which
    is the output of main_people_descriptors().
    '''
    os.system('python ./bayesequal.py -f ' + os.path.join(args.output_dir, ellas) + \
        ' -s ' + os.path.join(args.output_dir, ellos) + \
        ' -p ' + os.path.join(args.output_dir, total) + ' > ' + \
        os.path.join(args.output_dir, log))

def main(): 
	write_out_log_odds()                                     
	descriptor_log_odds()

if __name__ == '__main__':
    main()