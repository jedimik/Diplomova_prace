import argparse 
from tasks import Configuration, LoadData, Generator
from datetime import datetime
import time

def InfiniteLoop(args):
    while True:
        generate=LoadData()
        generate.start(config=args.config,datapath=args.data)


if __name__=="__main__":
    time.sleep(15) #wait 10 second to initialize database
    parser =  argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('-c','--config')
    parser.add_argument('-d','--data')
    args=parser.parse_args()    
    InfiniteLoop(args)
 


