import json
import argparse 
import sys
import random
import yaml
import os
import time
from influxdb import InfluxDBClient
from datetime import datetime

class Configuration(object):
        
    def load_config(self,filepath=None):    
        filepath = filepath or "config/config.yaml"
        file, ext = os.path.splitext(filepath)
        if ext==".yaml":
            return self.load_config_yaml(filepath)
        elif ext==".json":
            return self.load_config_json(filepath)  
        else:
            return None

    def load_config_json(self,filepath):    
        with open(filepath,'r',encoding="utf-8") as jsonfile:
            config=json.load(jsonfile)
        return config

    def load_config_yaml(self,filepath):    
        with open(filepath,'r',encoding="utf-8") as yamlfile:
            config=yaml.load(yamlfile,yaml.FullLoader)
        return config
    

class Generator(Configuration): #For generating simple values
    def generate(self,minvalue,maxvalue,datalength,outputname):
        df = [random.randint(minvalue,maxvalue) for x in range(datalength)] 
        with open("data/"+outputname,'w',encoding="utf-8") as outfile:
            dfs="\n".join([str(x) for x in df])
            #print(dfs)
            outfile.write(dfs)
    def main(self,config,datapath):
        self.generate(int(config['minvalue']),int(config['maxvalue']),int(config['datalength']),config['outputName'])

class LoadData(Configuration):
    def load_data(self,func,config,datapath=None):
        dataConf=config['data']
        dbConf=config['database']
        fifoConf=config['Predictor']
        db=DBconnect().LoadDB(dbConf)   
        if dataConf['generate']==True and datapath is None:
            Generator().main(dataConf,datapath="data/")
            return self.load_data_from_file(func,db,fifoConf, datapath="data/"+dataConf['outputName']) 
        elif dataConf['generate']==False and datapath is None:
             return self.load_data_from_file(func,db,fifoConf, datapath="data/outputData") 
        elif not datapath:
            return self.load_data_from_stdin(func,db,fifoConf)
        else:
            return self.load_data_from_file(func,datapath,fifoConf) 

    def load_data_from_file(self,func,db,config,datapath):
        with open(datapath,'r',encoding="utf-8") as datafile:
            for line in datafile:
                line=line.replace("\n","")
                func(line)
                time.sleep(1)
                #Send data DB
                DBconnect.SendToDB(self,db,PreprocessData().Process(line,False)) 
                #Send to fifo
                FifoSend().main(config,PreprocessData().Process(line,toStr=True))                    

    def load_data_from_stdin(self,func,db,config):
        for line in sys.stdin:
            line=line.replace("\n","")
            func(line)
            time.sleep(1)
            #Send data DB
            DBconnect.SendToDB(self,db,PreprocessData().Process(line,False))     
            #Send to fifo
            FifoSend().main(config,PreprocessData().Process(line,toStr=True))     

    def start(self,config,datapath):
        def my_func(line):
            print("Hodnota:",line)
        config=self.load_config(config)
        self.load_data(my_func,config,datapath=datapath)

class DBconnect(Configuration): 
    def LoadDB(self,config=None):    
        # establish connection to TnfluxDB
        client = InfluxDBClient(config["host"], config["port"], config["user"], config["pass"], config["database"])
        # create database if it does not exist
        client.create_database(config["database"])
        return client

    def SendToDB(self,client,data):
        client.write_points(data)

class FifoSend(Configuration):
    def confFifo(self,config): # For Predictor values
        if(config['send']==True):
            return self.openFifo(config)
        else:
            pass

    def openFifo(self,config):   
        return open(config['filepath'],'w',encoding="utf-8")
    
    def writeFifo(self,fifo,data):
        fifo.write(data)
        
    
    def main(self,config,data):
        fifo=self.confFifo(config)
        if fifo is not None:
            return self.writeFifo(fifo,data)        

class PreprocessData(Configuration):
    def Process(self,data,toStr=False):
        utctime = datetime.utcnow().isoformat()[:-3]
        json_body = [{
            "measurement": "Temperature",
            "time": utctime,
            "fields": {
            }
        }]
        field="Senzor1" #Simple for testing purposes
        json_body[0]["fields"][field] = float(data)
        if toStr:
            return json.dumps(json_body) #For fifo
        else:
            return json_body #For dtb
        