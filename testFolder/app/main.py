from influxdb import InfluxDBClient
from datetime import datetime
import random
import time
def InfiniteLoop():
    while True:
        utctime = datetime.utcnow().isoformat()[:-3]+'Z'
        json_body = [{
            "measurement": "Hodnota",
            "time": utctime,
            "fields": {
            }
        }]
        field="Teplota3" #Simple for testing purposes    
        client = InfluxDBClient("localhost",8086,"root","root","diplomka")
        json_body[0]["fields"][field] = random.randint(150,200)
        client.write_points(json_body)
        time.sleep(2)


if __name__=="__main__":    
    InfiniteLoop()
 


