import argparse
import json
import time
import argparse 
from tasks import ManageFifo

    
if __name__=="__main__":    
    parser =  argparse.ArgumentParser(description='-c for config')
    parser.add_argument('-c','--config')
    args=parser.parse_args()
    time.sleep(15) #wait for database
    ManageFifo().main(args)