import requests
import json
import os

# set working directory (windows)
os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the VT Cache directory
path_to_vtCache = cwd+"/DataDumps/virusTotal/"

# Function to request data from Virus total
def vt_url_getData(ip):
    
    # Defining the api-endpoint with the address on the end
    url = "https://www.virustotal.com/api/v3/ip_addresses/{}".format(ip)
    
    # Headers with api key
    # Get the API Secret
    # fr = File Read
    fr = open('api_secrets.json', 'r')
    vt_key = json.loads(fr.read())['api']['vt_key']
    # close the 
    fr.close()
    headers = {
        "Accept": "application/json",
        "x-apikey": vt_key
    }
    
    # return data to the request
    return requests.get(url, headers=headers)

# Function to pull from a file
def vt_file_getData(ip):
    file = open(path_to_vtCache+ip+'.json','r')
    data = json.loads(file.read())
    file.close()
    return data

# Function to handle VirusTotal API/File requests
def vt_xr_data(ip):
    # Check if the file exists
    if os.path.isfile(path_to_vtCache+ip+'.json') == 1:
        # call function to get the file
        vt_file = vt_file_getData(ip)

        return vt_file
    # if the file isn't there do an api call to get data and make file
    else:
        # call the cunctation that handles the api request to VT
        vt_api = vt_url_getData(ip)
        # Check if the return code is good
        if vt_api.status_code == 200:   
            # fx = file create
            # create the file with the ip.json
            fx = open(path_to_vtCache+ip+".json", 'x')
            # write the data from the api request to the new file
            fx.write(vt_api.text)
            # close the created file
            fx.close()
            # Check if the file was successfully created
            if os.path.isfile(path_to_vtCache+ip+'.json') == 1:
                # fr = file read
                # Read the newly made file
                fr = open(path_to_vtCache+ip+".json", 'r')
                # load the json values
                data = json.loads(fr.read())
                # close the file
                fr.close()
                return data
            else:
                return 1
        elif vt_api.status_code == 400:
            return 2
        elif vt_api.status_code == 404:
            return 3
        else:
            return 4