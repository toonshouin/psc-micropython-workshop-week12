from time import strftime
import csv
import time
import requests
from datetime import datetime

endpoint = "192.168.1.107"
endpoint_uri =  "http://{endpoint}/json"

def fetch():
    r = requests.get(endpoint_uri)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok",False):
        raise RuntimeError("Failed to fetch data, ESP32 return as not OK, {data}")
    return data

with open("temp_log.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if f.tell() == 0:
        w.writerow(["timestamp", "temp, hum_percent"])

    while True:
        try:
            data = fetch()
            ts = datetime.now.strftime("%Y-%m-%d %H:%M:%S")

            temp = data.get("temp", "")
            hum = data.get("hum", "")

            print(ts, temp, hum)
            w.writerow(ts,temp,hum)
            f.flush

        except Exception as e:
            print("Error, ", e)

        time.sleep(2)

