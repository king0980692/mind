import pickle

class encoder:
    
    def __init__(self, data, offset=0):
        self.idx = offset
        self.data = data

    def _unique(self):
        self.data = set(self.data)

        
    def _map_to_int(self):
        self.data.add('null')
        self.table = {val:i+self.idx for i, val in enumerate(self.data)}
        
        self.inverse_table = {val:i for i, val in self.table.items()}
        #return [table[v] for v in values]

    def _encode(self):
        return self._map_to_int()

    def fit(self):
        return self._encode()

    def transform(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return self.table['null']

if __name__ == '__main__':
    all_encoder = {}

    a_1 = set(['a','b','c'])
    a_2 = set(['1','2','3'])
    
    labels = [a_1, a_2]

    for i in range(2):
        all_encoder[i] = encoder(labels[i],len(labels[i]))
        all_encoder[i].fit()

    for i in range(2):
        enc = all_encoder[i]
        file_name = "./cached/test_pkl" + str(i) + ".pkl"
        with open(file_name,'wb') as f:
            pickle.dump(enc,f)


    for i in range(2):
        enc = all_encoder[i] 
        file_name = "./cached/test_pkl" + str(i) + ".pkl"
        with open(file_name,'rb') as f:
            p_enc = pickle.load(f)
            print(p_enc.table)
    