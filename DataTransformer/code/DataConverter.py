from code.Encoder import Encoder
from random import shuffle
from collections import defaultdict
import os, sys
import json
#from tqdm import tqdm

class DataConverter:

    def __init__(self, logger):
        self.logger = logger
        self.encoder = Encoder()
        pass

    def DataSplit(self, Input_list, outFile, action):

            operation, spliter = action 

            if spliter == '\\t':
                spliter = '\t'
            
            for iFile in Input_list:
                fname, cols, col_types, sep = iFile
                self.logger.info(f"{operation} the {cols}-th from {fname}")

               
                # Checking File Path 
                if not os.path.isfile(fname):
                    self.logger.error(f"{filePath} is not exit")
                    sys.exit()       
               
                # Checking output file, if exist delete it
                if outFile is not None and os.path.isfile(outFile):
                    os.remove(outFile)
               
                out_lines = []
                with open(fname, 'r') as f:

                    #for line in f.readlines():
                    #while (line := f.readline()):
                    line = f.readline()
                    while line:
                        line = line.rstrip().split(sep)
                        for idx, t_col in enumerate(cols):
                            if col_types[idx] == 'target':
                                split_item = line[t_col].split(spliter)
                                del line[t_col]
                                if operation == 'row_split':
                                    for _row in split_item:
                                        out = sep.join(line + [_row])
                                        # print(out)
                                        # sys.exit()                                        
                                        if outFile is not None:
                                            out_lines.append(out+"\n")
                                        else:
                                            self.logger.debug(out)

                                elif operation == 'col_split':
                                    out = sep.join(line + split_item)
                                    # print(out)
                                    # sys.exit()
                                    if outFile is not None:
                                        out_lines.append(out+"\n")
                                    else:
                                        self.logger.debug(out)
                        line = f.readline()
                        # print(out_lines)
                        # sys.exit()
                        with open(outFile, 'a') as of:
                            of.writelines(out_lines)
    
    


    def DataMap(self, Input_list, outFile):

         for iFile in Input_list:
            fname, cols, col_types, sep = iFile
            self.logger.info(f"Get dependency relation feature from {fname}")


            '''
                feat_mapper : 
                    dict of list, which map the target column to related feature
                    e.g.
                        feat_mapper['N12'] = {Sport, Baseball,  ...}

            '''

            
            feat_mapper = {}
            
            # Checking File Path
            if not os.path.isfile(fname):
                self.logger.error(f"{fname} is not exit")
                sys.exit()       
            


            with open(fname, 'r') as f:
                # TODO : ADD header flag to avoid read first line
                for index,line in enumerate(f):        
                    line = line.rstrip('\n').split(sep)

                    tmp_list = []
                    
                    # select the target col
                    for idx, t_col in enumerate(cols):
                        if col_types[idx] == 'target':
                            key_feat = line[t_col]
                           
                        elif col_types[idx] == 'cat':
                            tmp_list.append(line[t_col])

                    # store the related column into feat_mapper
                    feat_mapper[key_feat] = tmp_list


            self.logger.info(f"Output data map file to {outFile}")

            with open(outFile, "w") as f:
                f.write(json.dumps(feat_mapper, indent=4))


            
            
    def Data2sparse(self, Input_list, Mapfile):

        if Mapfile is not None:
            with open(Mapfile, newline='') as j:
                col_mapper = json.load(j)
            '''
            with open(Mapfile, newline='') as j:
                tmp_line = []
                for line in j.readlines():
                    dic = json.loads(line)
                    tmp_line.append(dic)
                col_mapper = json.load(j)
            '''
            
        total_unique_feat = []
        for iFile in Input_list:
            fname, cols, col_types, sep = iFile
            self.logger.info(f"Get unique feature from {fname}")
            

            '''
                unique_feat : 
                    dict of set, which map the selected column idx to feature
                    e.g.
                        unique[1] = {'U0','U1' ...}

            '''
            unique_feat = {}


            for idx in cols: unique_feat[idx] = []

            # Checking File Path
            if not os.path.isfile(fname):
                self.logger.error(f"{fname} is not exit")
                sys.exit()       
            


            with open(fname, 'r') as f:
                # TODO : ADD header flag to avoid read first line
                for index,line in enumerate(f):        
                    line = line.rstrip('\n').split(sep)
                    
                    # select the target col
                    for idx, t_col in enumerate(cols):
                        if col_types[idx] == 'cat':
                            unique_feat[t_col].append(line[t_col])
                        elif col_types[idx] == 'map':
                            #print(line[t_col])
                            #print(col_mapper[line[t_col]])
                            mapped_feat = col_mapper[line[t_col]]
                            if line[t_col] in col_mapper:
                                unique_feat[t_col].append(mapped_feat)

                        elif col_types[idx] == 'map-dynamic':
                            pass
                            #print(line[t_col])

                        

                        elif col_types[idx] == 'target':
                            unique_feat[t_col].append(line[t_col])
                            

                                
             
                print("check:",unique_feat)
                #label = "-".join([col,str(col)])
                total_unique_feat.append(unique_feat)

            #print(unique_feat)
            
        #print(total_unique_feat)

        '''
        for feats in total_unique_feat:
            for key, feats_vec in feats.items():
                self.encoder.encode_categorical(feats_vec,key)

        self.encoder.dump_map()
        print(self.encoder.idx)

        '''
                
    
    '''
    def data2lib(self):

    
    def DatatoLib(
            self, infile, outfile,
            target_column, sep,
            msep, offset, header,
            alpha, normalized, c_columns,
            n_columns, knn, process
   ):
   
        """
        Convert CSV data to libSVM/libFM format
        """

        self.logger.info("Load data")
        self.encoder.set_offset(offset)

        data = []

        k_columns = []
        for tp in knn:
            k, acolumn, bcolumn = tp.split(':')
            k_columns.append(int(acolumn))
        all_columns = c_columns + n_columns + k_columns

        unique_fea = {}
        for idx in c_columns: unique_fea[idx] = {}
        for idx in n_columns: unique_fea[idx] = {}
        for idx in k_columns: unique_fea[idx] = {}

        for fname in infile:
            self.logger.info("Get unique feature from '%s'" % (fname))
            with open(fname, 'r') as f:
                if header: next(f)
                for line in f:
                    line = line.rstrip('\n').split(sep)
                    # select the targer col
                    for idx in all_columns:
                        unique_fea[idx][line[idx]] = 1


        self.logger.info("Encode data")
        for idx in c_columns:
            label = 'Cat ' + str(idx)
            self.encoder.encode_categorical( unique_fea[idx].keys(), msep=msep, label=label )
            self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )
        for idx in n_columns:
            label = 'Num ' + str(idx)
            self.encoder.encode_categorical( unique_fea[idx].keys(), msep=msep, label=label )
            self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )
        for idx in k_columns:
            label = 'Sim ' + str(idx)
            self.encoder.encode_categorical( unique_fea[idx].keys(), msep=msep, label=label )
            self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )

        # KNN
        nn = {}
        if knn is not None:
            self.logger.info("Compute Similarity Feature")

            for tp in knn:
                tempnn = {}
                k, acolumn, bcolumn = map(int, tp.split(':'))
                nn[acolumn] = {}

                for a in unique_fea[acolumn].keys():
                    tempnn[a] = []

                with open(infile[0]) as f:
                    if header: next(f)
                    for line in f:
                        line = line.rstrip().split(sep)
                        tempnn[ line[acolumn] ].append(line[bcolumn])

                self.logger.info("Get column %d similarities based on column %d" % (acolumn, bcolumn))
                nn[acolumn] = self.fmaker.pairwise_similarity(tempnn, k, alpha, process=process)

        # Data Transforming
        converted = []
        dataout = []

        out = []
        for ifname, ofname in zip(infile, outfile):
            self.logger.info("Data Transforming on '%s' to '%s'" % (ifname, ofname))
            
            del converted[:]
            with open(ifname, 'r') as f:
                if header: next(f)
                
                for line in f:
                    del out[:]
                    line = line.rstrip('\n').split(sep)

                    out.append(line[target_column])

                    for idx in c_columns:
                        label = 'Cat ' + str(idx)
                        out.append( self.encoder.fit_categorical( line[idx], msep, label=label ) )

                    for idx in n_columns:
                        label = 'Num ' + str(idx)
                        out.append( self.encoder.fit_numeric( line[idx], label=label ) )

                    for idx in k_columns:
                        label = 'Sim ' + str(idx)
                        fea_vec = nn[idx][line[idx]] if line[idx] in nn[idx] else ""
                        out.append( self.encoder.fit_feature( fea_vec, msep='|', label=label, normalized=normalized ) )
                    
                    converted.append("%s" % (" ".join(out)))

            self.logger.info("Write encoded data to '%s'" % (ofname))
            with open(ofname, 'w') as f:
                f.write("%s\n" % ("\n".join(converted)))

   '''
