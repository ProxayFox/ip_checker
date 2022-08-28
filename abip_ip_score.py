import requests
import json
import os

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')
# Get the current working directory directory
cwd = os.getcwd()

def abip_url_getData(ip):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90',
        # 'verbose': 'true'
    }

    # Get the API Secret
    # fr = File Read
    fr = open('api_secrets.json', 'r')
    abip_key = json.loads(fr.read())['api']['abuseIP_key']
    fr.close()

    headers = {
        'Accept': 'application/json',
        'Key': abip_key
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output
    decodedResponse = json.loads(response.text)
    return json.dumps(decodedResponse, sort_keys=True, indent=4)

    # Formatted output
    # decodedResponse = json.loads(response.text)
    # return json.dumps(decodedResponse, sort_keys=True, indent=4)

# Function to pull from a file
def vt_file_getData(ip):
    file = open(path_to_abipCache+ip+'.json','r')
    data = json.loads(file.read())
    file.close()
    return data

# Grab the abip Cache directory
path_to_abipCache = cwd+"/DataDumps/abuseIP/"
ip = input("Enter The Ip :: ")
abip = abip_url_getData(ip)
# abip_json = json.loads(abip.text)
print(abip)



