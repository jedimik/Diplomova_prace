import numpy as np
import json
import os
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from scipy.stats import percentileofscore

class Configuration():      
    def load_config(self):    
        filepath = "config/config.json"
        file, ext = os.path.splitext(filepath)
        if ext==".json":
            return self.load_config_json(filepath)  
        else:
            return None

    def load_config_json(self,filepath):    
        with open(filepath,'r',encoding="utf-8") as jsonfile:
            config=json.load(jsonfile)
        return config
    
class InfluxDBClient():
    def __init__(self,config):
        self.config=config
        self.query_api=None
        #If not in swarm, than change config['url'] to config['urlLocal']
        self.client = influxdb_client.InfluxDBClient(
            url=self.config['url'], 
            token=self.config['token'],
            org=self.config['org']
        )
        self.write_api=self.client.write_api(write_options=SYNCHRONOUS)

    def send_to_database(self,data):
        self.write_api.write(self.config['bucket'],self.config['org'],{"measurement":self.config['measurementName'],
        "fields": {self.config['fieldName']:data}})
    
    def get_from_database(self,query_string):
        self.query_api=self.client.query_api()
        result = self.query_api.query(org=self.config['org'],query=query_string)
        return result
    
    def query_builder(self,config):
        query = ' from(bucket:"'+config['bucket']+'")\
|> range(start: '+config['time']+')\
|> filter(fn:(r) => r._measurement == "'+config['measurement']+'")\
|> filter(fn:(r) => r._field == "'+config['field']+'")'
        return query
    
    def query_builder_pred(self,config): #getting last value
        query = ' from(bucket:"'+config['bucket']+'")\
|> range(start: '+config['time']+')\
|> filter(fn:(r) => r._measurement == "'+config['measurement']+'")\
|> filter(fn:(r) => r._field == "'+config['field']+'")\
|> last()'
        return query

class LearnPred():
    def load_data(self,data):
        records=[]
        for table in data:
            for record in table.records:
                records.append(record.get_value())
        records.sort()
        records=np.array(records)
        return records

class Predict():
    def __init__(self,config):
        self.send_client=InfluxDBClient(config=config['sendData'])                

    def predict(self,learndata,value):
        result= percentileofscore(learndata, value)
        self.send_client.send_to_database(result)
        

class MainClass():
    def start_pred(self,config,records):
        predict_client=InfluxDBClient(config=config['predictDB'])
        prediction=Predict(config)
        while True:
            data=predict_client.get_from_database(query_string=predict_client.query_builder_pred(config['predictData']))      
            for table in data:
                for record in table.records:
                    value= record.get_value() 
            prediction.predict(records,value)       
    
    def start_learn(self,config):
        learn_client=InfluxDBClient(config=config['learnDB'])
        data=learn_client.get_from_database(query_string=learn_client.query_builder(config['learnData']))
        lp=LearnPred().load_data(data)
        return lp

    def start(self):
        #Load config
        cnf=Configuration().load_config()
        #Learn data
        lp=self.start_learn(cnf)
        #Predict data in loop       
        self.start_pred(cnf,lp)


if __name__=="__main__":
    time.sleep(10) #wait for establishing influxdb
    MainClass().start()

    