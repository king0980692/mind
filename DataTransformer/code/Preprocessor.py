class Preprocessor:

    def __init__(self):


   
    def join_data(self, feat_vec, label=None, isShared=False):
    
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


    
