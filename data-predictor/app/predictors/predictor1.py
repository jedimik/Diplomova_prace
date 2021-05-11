import json
import yaml
from influxdb import InfluxDBClient
from datetime import datetime,timedelta

class Prediction():
    def MultiplyPredict(self,data,config,db=None): #For simulation of prediction
        multiply=config["predictor1"]["multiplyValue"]
        data['value'] = multiply*float(data['value'])     
        return data





       
        

