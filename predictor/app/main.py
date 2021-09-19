import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

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

class ProcessData():
    def load_data(self,config):
        learn_db_conf=config['learnDB']
        learn_data_conf=config['learndata']
    
class InfluxDBClient():
    def __init__(self,config):
        self.config=config
        self.client = influxdb_client.InfluxDBClient(
            url=self.config['url'],
            token=self.config['token'],
            org=self.config['org']
        )
        self.write_api=self.client.write_api(write_options=SYNCHRONOUS)

    def send_to_database(self,data):
        data=influxdb_client.Point(self.config['measurementName']).field('fieldName',data)
        #self.write_api.write(bucket=self.config['bucket'],org=self.config['org'],record=data)

#Test purposes only
class Process():   
    def LoadData(self,config):
        database=config['learnDB']
        data=config['learndata']
        client = influxdb_client.InfluxDBClient(
   url=database['url'],
   token=database['token'],
   org=database['org']
)
        query_api = client.query_api()      
        query = ' from(bucket:"'+database['bucket']+'")\
|> range(start: '+data['time']+')\
|> filter(fn:(r) => r._measurement == "'+data['measurement']+'")\
|> filter(fn:(r) => r._field == "'+data['field']+'")'
        data = query_api.query(org=database['org'], query=query)
        result=0
        for table in data:
            for record in table.records:
                result+= record.get_value() # sum of all by time
        print(float(result))
        


if __name__=="__main__":
    cnf=Configuration().load_config()
    testpred=Process()
    data=testpred.LoadData(cnf)
    print(data)
    #print(type(test))
    