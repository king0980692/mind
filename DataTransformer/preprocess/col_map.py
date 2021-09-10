import argparse
import json
from sys import exit
import os

parser = argparse.ArgumentParser()


parser.add_argument('-i', "--input", default=None,
                    help="Target input file")

parser.add_argument('-t', "--target", default=None,
                    help="Target column for input data")

parser.add_argument('-s', "--sep", default=None,
                    help="Indicate the seperator to split the data")

parser.add_argument('-m', "--map", default=None,
                    help="Indicate the map file to map the column")


parser.add_argument('-o', "--output", default=None,
                    help="Indicate th output file")


config = parser.parse_args()


if config.input is None:
    raise ValueError("Please indicate the input file")
               
# Checking File Path 
if not os.path.isfile(config.input):
    print(f"{config.input} is not exit")
    exit()       

if config.output is None:
    raise ValueError("Please indicate the output file")

# check tab seperator case
if config.sep == '\\t':
    config.sep = '\t'

# check the target line length
config.target = int(config.target)


map_dict = None
with open(config.map, 'r') as f:
    map_dict = json.load(f)   

if map_dict is None:
    raise ValueError("Please indicate the correct map file")




out_lines = []
with open(config.input, 'r') as f:
    
    line = f.readline()

    while line:
        line = line.rstrip('\n').split(config.sep)
        mapped_item = " ".join(map_dict[line[config.target]])
        line.insert(config.target+1, mapped_item)

        out = config.sep.join(line)

        out_lines.append(out+"\n")

        line = f.readline()
        
with open(config.output, 'w') as of:
    of.writelines(out_lines)
        
