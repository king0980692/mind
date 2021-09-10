import argparse
from sys import exit
import pickle

class encoder:
    def __init__(self) -> None:
        self.idx = 0
        self.keymap = {}
        
        self.shared_keymap = {}
        self.data = None

    def _unique(self, y):
        return list(set(y))
        
    
    def _encode(self, values, tag):

        for v in values:
            key = (v, tag)
            if v not in self.keymap:
                self.keymap[key] = self.idx
                self.idx +=1
    
    def fit(self, y, tag):
        self.data = self._unique(y)
        self._encode(self.data, tag)
        return self

    def transform(self, y, tag, shared_flag=False):
            
        if self.keymap == None:
            raise ValueError("data must be fit first \n")

        if not isinstance(y, list):
            y = [y]

        shared_idx = self.idx
        unseen_label = False
        out = []
        for item in y:
            key = (item, tag)
            if key in self.keymap:
                out.append(self.keymap[key])
            elif shared_flag:
                unseen_label = True
                self.shared_keymap[key] = shared_idx
                out.append(shared_idx)
            else:
                raise ValueError(f"Unseen label : {item}\n")

        if shared_flag and unseen_label:
            self.idx += 1
        
        
        return out


if __name__ == '__main__':

    # fake target line
    target_line = [1, 4]

    '''

    # fake read file
    # feat_list := dict of list
    feat_list = {t:set() for t in target_line}




    with open("../data/beh_split4.tsv", 'r') as f:

        line = f.readline()
        while line:
            line = line.rstrip().split('\t')

            for t in target_line:
                # 1D case
                if len(line[t].split()) > 1:
                     for ll in line[t].split():
                        feat_list[t].add(ll)
                # 0D case
                else:
                    feat_list[t].add(line[t])

            line = f.readline()
    
    print("1")
    # fake encoder class test

    enc = encoder()
    for col, feat in feat_list.items():
        enc.fit(feat,col)
    
    print("2")

    with open("./encoder.class",'wb') as f:
        pickle.dump(enc, f)
    
    print(enc.keymap)
    
    exit()
    '''
    
    with open("./encoder.class", 'rb') as f:
        enc = pickle.load(f)
    

    out_lines = []
    truth_idx = 7
    with open("../data/beh_split4.tsv", 'r') as f:
        line = f.readline()
        
        while line:        
            line = line.rstrip().split('\t')

            y = line[truth_idx]

            out = []
            for t in target_line:
                # 1D case
                if len(line[t].split()) > 1:
                    out+= enc.transform(line[t].split(), t, shared_flag=False)
                # 0D case
                else:

                    out+= enc.transform(line[t], t, shared_flag=False)
                    #out+=(enc.transform(line[t], t, shared_flag=True))
            
            out = " ".join("{}:1".format(o) for o in out)
            out = y + " " + out + "\n"
            out_lines.append(out)            

            line = f.readline()    
        
    with open("./output.txt", 'w') as of:
        of.writelines(out_lines)