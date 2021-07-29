import random
import json
import influxdb_client
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

class Configuration(object):       
    def load_config(self,filepath=None):    #Load config json or yaml
        filepath = filepath or "config/config.json"
        return self.load_config_json(filepath)

    def load_config_json(self,filepath):    
        with open(filepath,'r',encoding="utf-8") as jsonfile:
            config=json.load(jsonfile)
        return config

class Generate():
    def Start(self,config):
        client=influxdb_client.InfluxDBClient(
            url=config["url"],
            token=config["token"],
            org=config["org"]
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        while True:
            time.sleep(1)
            number=random.randint(100,150)
            print("Generuju: ",number)
            data=influxdb_client.Point("mereni").field("hodnota",number)
            write_api.write(bucket=config["bucket"],org=config["org"],record=data)                       
            print("Zapsal jsem: ", number)


if __name__=="__main__":
    cnf=Configuration().load_config()
    cnf=cnf['database']
    print("tu")
    gen=Generate()
    gen.Start(config=cnf)
