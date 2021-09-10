#!/bin/bash

# 0. Generate the **map file** using below instruction
python3 ./preprocess/gen_map.py -i ../data/news.tsv -k 0 -t 1,2 -s '\t' -o ./map.json

# 1. **Row split** the impression column
python3 ./preprocess/row_split.py -i ../data/behaviors.tsv -t 4 -s '\t' -d ' ' -o ../data/beh_split.tsv

# 2. **Column split** the impression column
python3 ./preprocess/col_split.py -i ../data/beh_split.tsv -t 4 -s '\t' -d '-' -o ../data/beh_split2.tsv

# 3. **Column map** the News ID column
python3 ./preprocess/col_map.py -i ../data/beh_split2.tsv -t 4 -s '\t' -m ./map.json -o ../data/beh_split3.tsv

# 4. **Column split** at the mapped column
python3 ./preprocess/col_split.py -i ../data/beh_split3.tsv -t 5 -s '\t' -d ' ' -o ../data/beh_split4.tsv
