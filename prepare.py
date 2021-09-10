from multiprocessing import Pool
from tqdm import tqdm
import sys
import argparse
import random
import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import scipy

labelencoder = LabelEncoder()


news_feat_map = {}

newsID_set = set()
userID_set = set()
hisID_set = set()

cat_map = {}
cat_set = set()

subcat_map = {}
subcat_set = set()

title_map = {}
title_set = set()


feat_list = list()


train_dir = "../train/"
dev_dir = "../dev/"
test_dir = "../test/"

train_beh = os.path.join(train_dir, "behaviors.tsv")
train_news = os.path.join(train_dir, "news.tsv")

dev_beh = os.path.join(dev_dir, "behaviors.tsv")
dev_news = os.path.join(dev_dir, "news.tsv")

test_beh = os.path.join(test_dir, "behaviors.tsv")
test_news = os.path.join(test_dir, "news.tsv")


def decision(probability):
    return random.random() < probability


def gen_data(_type, pos):

    _dir = "./" + _type + "_dir/"
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    _txt = _dir + _type + ".txt"
    if os.path.isfile(_txt):
        os.remove(_txt)

    if _type == "train":
        _beh = "../train/behaviors.tsv"
    elif _type == "dev":
        _beh = "../dev/behaviors.tsv"
    elif _type == "test":
        _beh = "../test/behaviors.tsv"

    onehot_df = pd.DataFrame()
    headers = []
    # feat_list = ['user_id','news_id','news_cat','news_subcat']
    
    '''
        Generate the one-hot indexing label by pandas get_dummies
        which will cost lots of time
    ''' 
    for feat_set in tqdm(feat_list):

        # get the feature name from dict
        feat_name = next(iter(feat_set))
        
        tmp_df = pd.DataFrame(columns=[feat_name])
        tmp_df[feat_name] = list(feat_set[feat_name])
        tmp_df = pd.get_dummies(tmp_df, prefix=[""], prefix_sep="", sparse=True)

        headers = headers + tmp_df.columns.tolist()



    onehot_df = pd.DataFrame(columns=headers)

    with open(_beh) as f:
        pbar = tqdm(
            f.readlines(),
            position=pos,
            colour="red",
            desc="Generating the " + _type + ".txt",
            leave=False,
        )

        for idx, line in enumerate(pbar):

            l = line.rstrip().split("\t")
            user_id, history, impressions = l[1], l[3].split(), l[-1]

            for imp in impressions.split():
                if _type == "train":
                    news_id, isclick = imp.split("-")
                    # drop 80 percent of zeros data
                    if isclick == "0" and decision(0.8):
                        continue
                elif _type == "dev":
                    news_id, isclick = imp.split("-")

                elif _type == "test":
                    news_id = imp

                # this news' feature
                if news_id in news_feat_map:
                    news_cat = news_feat_map[news_id]["news_cat"]
                    


                output = []
                for feat_set in feat_list:
                    feat_name = next(iter(feat_set))

                    # get the index of feature 
                    index = onehot_df.columns.get_loc(eval(feat_name))
                    output.append(index)

                feature = " ".join("{}:1".format(out) for out in output)

                print(
                    feature,
                    file=open(_txt, "a+"),
                )



def extra_feature(feature):

    sys.stderr.write("Finish ...\n\n")

    # extract the USER's info
    for beh in [train_beh, dev_beh, test_beh]:
        with open(beh) as f:
            pbar = tqdm(
                f.readlines(),
                colour="blue",
            )
            for idx, line in enumerate(pbar):
                l = line.rstrip().split("\t")
                user_id, history, impressions = l[1], l[3].split(), l[-1]
                impressions = [imp.split("-")[0] for imp in impressions.split()]
                if feature["users_id"]:
                    userID_set.add(user_id)
                    # for h in history:
                    #     newsID_set.add(h)
                    # for imp in impressions:
                    #     newsID_set.add(imp)

    # extract the ITEM's info
    for news in [train_news, dev_news, test_news]:
        with open(news) as f:
            for line in tqdm(f.readlines(), colour="cyan"):
                l = line.rstrip().split("\t")
                
                news_id = l[0]
                news_cat = l[1]
                news_subcat = l[2]

                # news_title = json.loads(l[6])
 
                news_feat_map[news_id] = {}
                
                newsID_set.add(news_id)
                cat_set.add(news_cat)
                subcat_set.add(news_subcat)
            
                news_feat_map[news_id]["news_cat"] = news_cat            
                news_feat_map[news_id]["news_subcat"] = news_subcat



    sys.stderr.write("Finish ...\n\n")


def prepare_data(args):
    possible_feat = vars(args)
    # del possible_feat["train"]
    # del possible_feat["dev"]
    # del possible_feat["test"]

    # keep this order of feature
    
    if possible_feat["users_id"]:
        feat_list.append({"user_id": userID_set})
    if possible_feat["news_id"]:
        feat_list.append({"news_id": newsID_set})
    if possible_feat["news_cat"]:
        feat_list.append({"news_cat": cat_set})
    if possible_feat["news_subcat"]:
        feat_list.append({"news_subcat": subcat_set})

    extra_feature(possible_feat)

    if possible_feat["train"]:
        gen_data("train", 0)
    elif possible_feat["dev"]:
        gen_data("dev", 0)
    elif possible_feat["test"]:
        gen_data("test", 0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--dev", action="store_true")
    parser.add_argument("--test", action="store_true")

    parser.add_argument("--news_id", dest="news_id", action="store_true", default=False)
    parser.add_argument(
        "--users_id", dest="users_id", action="store_true", default=False
    )
    parser.add_argument(
        "--news_cat", dest="news_cat", action="store_true", default=False
    )
    parser.add_argument(
        "--news_subcat", dest="news_subcat", action="store_true", default=False
    )

    args = parser.parse_args()

    prepare_data(args)

    sys.exit(0)

