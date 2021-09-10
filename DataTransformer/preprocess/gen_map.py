import argparse
import json
from sys import exit

parser = argparse.ArgumentParser()


parser.add_argument('-i', "--input", default=None,
                    help="Target input file")

parser.add_argument('-k', "--key", default=None,
                    help="Key column for input data")

parser.add_argument('-t', "--target", default=None,
                    help="Target column for input data")

parser.add_argument('-s', "--sep", default=None,
                    help="Indicate th seperator to split the data")

parser.add_argument('-o', "--output", default=None,
                    help="Indicate th output file")


config = parser.parse_args()


if config.input is None:
    raise ValueError("Please indicate the input file")

if config.output is None:
    raise ValueError("Please indicate the output file")


# check tab seperator case
if config.sep == '\\t':
    config.sep = '\t'

# check the target line length
config.target = config.target.split(',')
config.target = [int(t) for t in config.target]

# check the key column

config.key = int(config.key)


with open(config.input, 'r') as f:
    line = f.readline()

    out = {}
    while line:
        line = line.rstrip('\n').split(config.sep)

        key = line[config.key]
        values = []
        for idx, target in enumerate(config.target):

            # handle the column is list situation
            if type(line[target] is list):
                for v in line[target].split():
                    values.append(v)
                    #record[idx].add(_fea)

            # handle the one column situation
            else:
                values.append(line[target])
        
        out[key] = values
        line = f.readline()

    
    with open(config.output, 'w') as j:
        json.dump(out,j)
        
        

