import argparse, logging , sys
from code.DataConverter import DataConverter



def main():

    DC = DataConverter(logger)
    
    if CONFIG.Task == 'data2sparse':
        
        DC.Data2sparse(CONFIG.InputInfo, CONFIG.Mapfile)
        
        
    elif CONFIG.Task == 'dataMap':
        DC.DataMap(CONFIG.InputInfo,CONFIG.OutputFileName)
        
    elif CONFIG.Task == 'dataSplit':
        DC.DataSplit(CONFIG.InputInfo,CONFIG.OutputFileName,CONFIG.Action)
    else:
        logger.error("Unknow Task")


    logger.info(f"Task-{CONFIG.Task} Completed")
    

# ----------------------

if __name__ == '__main__':

    """

    Check Arguments 

    """
    
    
    # Arguments
    PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                        usage="python DataEncode.py -task [Task] -infile [InputFile] -outfile [Outputfile] [Options]")
    
    # Some default setting
    PARSER.add_argument('--offset', dest='Offset',default=1,
                        help="Encoding start index (default=1).")
    
    
    PARSER.add_argument('--nproc', dest='Process',default=1,
                        help="The number of process used in this task.")
    
    
   
    
    # Tasks 
    task_list = ['dataMap','data2sparse','dataSplit']
    PARSER.add_argument('-t','--task', dest='Task', default=None,
                        help=f"Specify the task. Options: {task_list}.")

    
    # files
    PARSER.add_argument('-i','--infile', dest='InputInfo', default=None,
                        action='append',nargs='*',help="[InputFileName] [col_1,col2,...] [col_type1,col_type2..]")


    PARSER.add_argument('-o','--outfile', dest='OutputFileName', default=None,
                        help="Output File Name. ")
    
    '''   
    PARSER.add_argument('--header', dest='Header',type=int, default=None,
                        help="With header or not. ")
    '''              
    


    PARSER.add_argument('-a','--action', dest='Action', default=None,
                        nargs='+',help="The data you wanted operation. ")

    

    PARSER.add_argument('-m','--mapfile', dest='Mapfile', default=None,
                        help="The data you wanted operation. ")

    
    
    
    
    
    #PARSER.set_defaults(argument_default=False)

    CONFIG = PARSER.parse_args()

    logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                        level=logging.DEBUG,
                        datefmt='%m/%d/%y %H:%M:%S')


    logger = logging.getLogger( __name__ )
    logger.info("Arguments Check")



    # Task check
    if CONFIG.Task is not None:
        if CONFIG.Task not in task_list:
            logger.error("Unknow Task.")
            logger.error(f"Options: {task_list}")
            sys.exit()
        logger.info(f"Task: {CONFIG.Task}")
    else:
        logger.error("Please Specify the Task.")
        logger.error(f"Options: {task_list}")
        sys.exit()

   
    ''' 
        --- Input file check ---

        input file structure :
        
            [filename] [col_1,col_2...] [colType_1,colType_2] [Seperator]

            (the len of columns must be equal to column Types)
    '''
    
    if CONFIG.InputInfo is not None:

        Input_list = []
        colType_list = ['cat','target','num','map','map-dynamic']

        if CONFIG.Task == 'data2sparse' or CONFIG.Task == 'dataMap':
        
            # Input Info : [filename],[cols],[colType],[sep]
            for Ifile in CONFIG.InputInfo:
                if len(Ifile) != 4:
                    logger.error("Input format is : [filename] [cols] [colType] [sep]  (seprated by space)")
                   
                    logger.error("e.g.  --task 'data2sparse' -i ./test.tsv 4,5 map,target \'\\t\' ")

                    sys.exit()
                cols = Ifile[1].split(',')

                # Check cols must be numerical data
                for _col in cols:
                    if not _col.isdigit():
                        logger.error(f"col should be a numerical data, but got \"{_col}\"")
                        sys.exit()
                        
                cols = [int(c) for c in cols]

                col_types = Ifile[2].split(',')
                if 'map' in col_types:
                    if CONFIG.Mapfile is None:
                        logger.error("map colType is setted, you need to indicate the map file")
                        sys.exit()
                        
                # must have "target' type
                if 'target' not in col_types:
                    logger.error(f"colType must be have target type")
                    sys.exit()

                                
                # Check col_types must be one of colType in colType_list 
                for _type in col_types:
                    
                    if _type not in colType_list:
                        logger.error(f"colType must be one of {colType_list}")
                        sys.exit()
                    
                
                if len(cols) != len(col_types):
                    logger.error("number of col must be equal to number of colTypes")
                    sys.exit()
                
                # Checking Seperator
                if Ifile[3] =='\\t':
                    Ifile[3] = '\t'
                

                Input_list.append([Ifile[0], cols , col_types, Ifile[3]])



        elif CONFIG.Task == 'dataSplit':
            
            if CONFIG.Action is None:
               logger.error(f"Task dataSplit need to indicate an action .")
               sys.exit()
                
            if len(CONFIG.Action) != 2:
               logger.error("Action formate is:   [action],[sep] ")
                   
               sys.exit()            


            action_list = ['row_split','col_split']
            
            if CONFIG.Action[0] not in action_list:
                logger.error(f"Action error ")
       
                logger.error(f"Available action is {action_list}")
                sys.exit()
                
   
            # Input Info : [filename],[cols],[colType],[sep]
            for Ifile in CONFIG.InputInfo:
                if len(Ifile) != 4:
                    logger.error("Input format is : [filename] [cols] [colType] [sep]  (seprated by space)")
                   
                    logger.error("e.g.  --task 'data2sparse' -i ./test.tsv 4,5 map,target '\t'")
                    sys.exit()
                cols = Ifile[1].split(',')

                # Check cols must be numerical data
                for _col in cols:
                    if not _col.isdigit():
                        logger.error(f"col should be a numerical data, but got \"{_col}\"")
                        sys.exit()
                        
                cols = [int(c) for c in cols]

                col_types = Ifile[2].split(',')

                
                # must have "target' type
                if 'target' not in col_types:
                    logger.error(f"colType must be have target type")
                    sys.exit()

                                
                # Check col_types must be one of colType in colType_list 
                for _type in col_types:
                    
                    if _type not in colType_list:
                        logger.error(f"colType must be one of {colType_list}")
                        sys.exit()
                    
                
                if len(cols) != len(col_types):
                    logger.error("number of col must be equal to number of colTypes")
                    sys.exit()
                
                # Checking Seperator
                if Ifile[3] =='\\t':
                    Ifile[3] = '\t'
                

                Input_list.append([Ifile[0], cols , col_types, Ifile[3]])
        
        CONFIG.InputInfo = Input_list
        
        logger.info(f"Input File: {CONFIG.InputInfo}")
    else:
        logger.error("Please specify input files splitted by ' '")
        logger.error("e.g. --infile \"[Input filename] [columns] [columnTypes] [Seperator] ...\"")
        sys.exit()


    # Output file check
    if CONFIG.OutputFileName is not None:
        CONFIG.OutputFileName = CONFIG.OutputFileName
        if len(CONFIG.OutputFileName.split(',')) != 1:
            logger.error("Only support one ouput file.")
            sys.exit()
        logger.info(f"Output File: {CONFIG.OutputFileName}")
    else:
        logger.warning("No indicate output file, task will output on stdout")
        
        logger.warning("Or you need to indicate output file")
        logger.warning("e.g. --outfile [OutputFile] ")
       

    ''' 
    if CONFIG.TargetColumn is not None:
        logger.info(f"Target Column: {CONFIG.TargetColumn}")
    else:
        logger.error("Please specify the InputFile name and target column.")
        logger.error("e.g. --target [InputFile]:[Target Column]")
        sys.exit()

    if CONFIG.Separator is not None:
        logger.info(f"Separator: {CONFIG.Separator}")
        if CONFIG.Separator == "\\t": CONFIG.Separator = "\t"
    else:
        logger.error("Please specify the separator.")
        logger.error("e.g. --sep ','")
        sys.exit()

    if CONFIG.Header is not None:
        logger.info(f"Header: {CONFIG.Header}")
    else:
        logger.warning("Default Header: '0' (no header)")
        CONFIG.Header = False





    if CONFIG.Offset is not None:    
        logger.info(f"Offset: {CONFIG.Offset,} (encoding index starts from {CONFIG.Offset})")
    else:
        logger.info("Offset: '1' (encoding index starts from 1)")
        CONFIG.Offset = 1

    if CONFIG.Process is not None:
        CONFIG.Process = int(CONFIG.Process)
        logger.info(f"Number of Process: {CONFIG.Process}")
    else:
        logger.info("Number of Process: '1' (encoding index starts from 1)")
        CONFIG.Process = 1

    

    '''
    logger.info("Task Start")

    main()
    
