from tqdm import tqdm
import numpy as np
import pickle
import random
import sys
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, help="predict file")
args = parser.parse_args()

score_list = []

if "dev" in args.file:
    with open("./dev_output.txt", "r") as o:
        for line in tqdm(o):
            score = line.rstrip("\n")
            score_list.append(score)
elif "test" in args.file:
    with open("./test_output.txt", "r") as o:
        for line in tqdm(o):
            score = line.rstrip("\n")
            score_list.append(score)


test_dict = {}

total = 0
cnt = 0


idx = 0


with open(args.file, "r") as f:
    for line in tqdm(f):
        impression, uid, time, history, targets = line.rstrip("\n").split("\t")
        # print("\n",targets)
        if "test" in args.file:
            targets = targets.split(" ")
        elif "dev" in args.file:
            targets = targets.split(" ")
            targets = [t.split("-")[0] for t in targets]
        # uid = uid[1:]
        target_len = len(targets)
        # print(target_len)
        target_score = score_list[idx : idx + target_len]
        # print(idx,idx + target_len)
        # print(len(target_score))
        idx += target_len
        # print(idx)
        targets = [t for t in targets]

        targets = [float(target_score[i]) for i in range(target_len)]
        # print(targets)

        sort_targets = sorted(targets, reverse=True)

        tmp_list = [str(sort_targets.index(t) + 1) for t in targets]
        sep = ","
        ranks = f"[{sep.join(tmp_list)}]"
        print(f"{impression} {ranks}")
