import requests
import json
import os

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')
# Get the current working directory directory
cwd = os.getcwd()

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'

querystring = {
    'ipAddress': '118.25.6.39',
    'maxAgeInDays': '90',
    # 'verbose': 'true'
}
file = open('api_secrets.json', 'r')
vt = json.loads(file.read())
key = vt['api']['abuseIP_key']
headers = {
    'Accept': 'application/json',
    'Key': key
}

response = requests.request(method='GET', url=url, headers=headers, params=querystring)

# Formatted output
decodedResponse = json.loads(response.text)
print(json.dumps(decodedResponse, sort_keys=True, indent=4))