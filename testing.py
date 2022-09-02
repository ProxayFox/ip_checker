# Testing URLScan

import requests
import json

fr = open('api_secrets.json', 'r')
vt_key = json.loads(fr.read())['api']['urlScan_key']
# close the 
fr.close()

headers = {
    'API-Key': vt_key,
    'Content-Type': 'application/json'
}
data = {
    "url": "http://breckcraigint.pro",
    "visibility": "public"
    }
response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))

decodedResponse = json.loads(response.text)
urlscan_api_formatted = json.dumps(decodedResponse, sort_keys=True, indent=4)

# print(response)
# print(response.json())
print(urlscan_api_formatted)