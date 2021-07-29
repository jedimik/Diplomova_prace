import json
import argparse 
import sys
import random
import yaml
import os
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

class Configuration(object):       
    def load_config(self,filepath=None):    #Load config json or yaml
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

class LoadData(Configuration): # Load data for generating
    def load_data(self,func,config,datapath=None):
        dataConf=config['data']
        dbConf=config['database']
        db=DBconnect().LoadDB(dbConf)   
        if dataConf['generate']==True and datapath is None: #Generate new data and load them
            Generator().main(dataConf,datapath="data/")
            return self.load_data_from_file(func,db,dbConf, datapath="data/"+dataConf['outputName']) 
        elif dataConf['generate']==False and datapath is None: #Load data from datapath 
             return self.load_data_from_file(func,db,dbConf, datapath="data/outputData") 
        else:   
            pass

    def load_data_from_file(self,func,db,config,datapath):
        with open(datapath,'r',encoding="utf-8") as datafile:
            for line in datafile:
                line=line.replace("\n","")
                func(line)
                time.sleep(1)
                #Send data DB
                DBconnect.SendToDB(self,config,db,PreprocessData().Process(line,False))                 

    def load_data_from_stdin(self,func,db,config):
        for line in sys.stdin:
            line=line.replace("\n","")
            func(line)
            time.sleep(1)
            #Send data DB
            DBconnect.SendToDB(self,config,db,PreprocessData().Process(line,False))        

    def start(self,config,datapath):
        def my_func(line):
            print("Hodnota:",line)
        config=self.load_config(config)
        self.load_data(my_func,config,datapath=datapath)

class DBconnect(Configuration): 
    def LoadDB(self,config=None):    
        # establish connection to TnfluxDB
        client = influxdb_client.InfluxDBClient(url=config["url"],token=config["token"],org=config["org"])
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # create database if it does not exist
        return write_api

    def SendToDB(self,config,db,data):
        db.write(bucket=config["bucket"],org=config["org"],record=data)    

class PreprocessData(Configuration):
    def Process(self,data,toStr=False):
        #Lze nakonfigurovat, zatim test
        data=influxdb_client.Point("testovaci_mereni").field("senzor1",float(data))
        return data
        