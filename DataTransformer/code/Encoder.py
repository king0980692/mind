class Encoder:

    def __init__(self):
        self.idx = 0
        self.keymap = {}
        self.label_len = {}

    def set_offset(self, offset):
        self.idx = int(offset)

    # def get_max_idx(self):
    #     print(self.idx)
    #     print(type(self.idx))
    #     return self.idx

    def get_label_len(self, label):
        return self.label_len[label]

    def encode_categorical(self, feat_vec, label=None, isShared=False):
        """
        Encode for categorical features

            self.keymap is a dict, which map feat into idx

            e.g. 
                    {('user', 'U0')} -> 0
    
        """
        
        idx_init = self.idx
        for feat in feat_vec:
            key = (label,feat)
            
            # Encounter the new feat, so add into the keymap
            if key not in self.keymap:
                self.keymap[key] = self.idx
                self.idx += 1
            
        if isShared:
            key = (label, "_".join([label,"shared"]))
            self.keymap[key] = self.idx
            self.idx += 1
    
        #print(self.keymap)
        #print(self.idx)
        #self.label_len[label] = self.idx - idx_init

    def dump_map(self, outfile=None):
        out = []
        for key in self.keymap.keys():
            print(f"{key} {self.keymap[key]}")
            # out.append("%s %s" % (key, self.keymap[key]))
        # fout = open(mfile, 'w')
        # fout.write("\n".join(out))
        # fout.close()


    
