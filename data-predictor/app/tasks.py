import json
import sys
import yaml
import os
import time
import csv
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from predictors.predictor1 import Prediction

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

class DBconnect(Configuration): 
    def loadDB(self,config=None):    
        # establish connection to TnfluxDB
        client = InfluxDBClient(config["host"], config["port"], config["user"], config["pass"], config["database"])
        # create database if it does not exist
        client.create_database(config["database"])
        return client

    def sendToDB(self,client,data):
        client.write_points(data)

class PreProcess(): #get only timestamp and value
    def ProcessJson(self,data): #Just for json
        line = json.loads(data)
        data = {'timestamp':line[0]["time"],'value':line[0]["fields"]["Senzor1"]}
        return data

    def ProcessDB(self,data,config): #for
        utctime = data['timestamp'] #pred for 5second in future
        json_body = [{
            "measurement": config['valueAs'],
            "time": utctime,
            "fields": {
            }
        }]
        field="Senzor1" #Simple for testing purposes
        json_body[0]["fields"][field] = float(data['value'])
        return json_body #For dtb

class ManageFifo(Configuration):
    def read_from_fifo(self,config):                                     
        fIN=self.openFifo(config['Predictor']['filepath'],'r')           
        for data in fIN: 
            data=data.strip()
            if data:
                #print(data)
                newData=PreProcess().ProcessJson(data)
                return newData 
        fIN.close()
                                                            

    def openFifo(self,path, mode):
            return open(path,mode,encoding="utf-8")
    
    def main(self,args=None):
        if args is not None:
            config=self.load_config(filepath=args.config)
        else: #Default config       
            config=self.load_config('config/config.json')
        #Establish dtb connect before while
        db=DBconnect().loadDB(config['database'])    
        while True:
            #Get data from fifo and preprocess        
            data = self.read_from_fifo(config)
            #For predict
            predData=Prediction().MultiplyPredict(data,config)
            DBconnect.sendToDB(self,db,data=PreProcess().ProcessDB(predData,config['predictor1']))
            time.sleep(1)

