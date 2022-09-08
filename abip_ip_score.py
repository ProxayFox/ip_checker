import requests
import json
import os

# set working directory (windows)
os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the ABIP Cache directory
path_to_abipCache = cwd+"/DataDumps/abuseIP/"

def abip_url_getData(ip):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90',
        'verbose': 'true'
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

    return requests.request(method='GET', url=url, headers=headers, params=querystring)

# Function to pull from a file
def abip_file_getData(ip):
    file = open(path_to_abipCache+ip+'.json','r')
    data = json.loads(file.read())
    file.close()
    return data

def abip_xr_data(ip):
    # Check if the file exists
    if os.path.isfile(path_to_abipCache+ip+'.json') == 1:
        abip_file = abip_file_getData(ip)
        return abip_file
    else:
        abip_api = abip_url_getData(ip)
        if abip_api.status_code == 200:
            # format the returned results
            decodedResponse = json.loads(abip_api.text)
            abip_api_formatted = json.dumps(decodedResponse, sort_keys=True, indent=4)

            # fx = file create
            # create the file with the ip.json
            fx = open(path_to_abipCache+ip+".json", 'x')
            # write the data from the api request to the new file
            fx.write(abip_api_formatted)
            # close the created file
            fx.close()
            # Check if the file was successfully created
            if os.path.isfile(path_to_abipCache+ip+'.json') == 1:
                # fr = file read
                # Read the newly made file
                fr = open(path_to_abipCache+ip+".json", 'r')
                # load the json values
                data = fr.read()
                # close the file
                fr.close()
                return json.loads(data)
            else:
                return 1
        elif abip_api.status_code == 400:
            return 2
        elif abip_api.status_code == 404:
            return 3
        else:
            return 4