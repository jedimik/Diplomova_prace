import json
import sys
import os
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class Configuration(object):      
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

class Process():   
    def LoadData(self,config):
        database=config['database']
        data=config['data']
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
        result = query_api.query(org=database['org'], query=query)
        return result
    
    def SendToDatabase(self,config,data):
        time.sleep(1) # every second
        client=influxdb_client.InfluxDBClient(
            url=config["url"],
            token=config["token"],
            org=config["org"]
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data=influxdb_client.Point("predikce").field("hodnota",data)
        write_api.write(bucket=config["bucket"],org=config["org"],record=data)                      

    def Predict(self,config): #For simulation of prediction
        result=0
        data=self.LoadData(config)        
        for table in data:
            for record in table.records:
                result+= record.get_value() # sum of all by time
        result/=20 #example value by 20s
        result*=float(config['predictor']['multiply'])
        print("predikuji:",result) 
        return self.SendToDatabase(config['database'],result)

if __name__=="__main__":    
    cnf=Configuration().load_config()
    time.sleep(10) #wait for database
    pred=Process()
    while True:
        pred.Predict(cnf)

