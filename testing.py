# Testing URLScan
import requests
import json
import os

# set working directory (windows)
os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the urlScan Cache directory
path_to_urlScan_Cache = cwd+"/DataDumps/urlScan/"

# Grab data from the API
def urlscan_URL_GetData(url):
    # Open file with the api key
    fr = open('api_secrets.json', 'r')
    vt_key = json.loads(fr.read())['api']['urlScan_key']
    # close the 
    fr.close()

    headers = {
        'API-Key': vt_key,
        'Content-Type': 'application/json'
    }
    data = {
        "url": url,
        "visibility": "public"
        }

    # Get the response from URLScan
    # Return to request with the decode plus more making it better to view the data
    return requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))     

#  Grab file and read the data
def urlScan_file_getData(url):
    # Grab File and set to read
    file = open(path_to_urlScan_Cache+url+'.json','r')
    # Read the file and load json
    data = json.loads(file.read())
    # Format the data to be readable
    data_format = json.dumps(data, sort_keys=True, indent=4)
    # Close the file
    file.close()
    # Return with the files data
    return data_format

def urlScan_xr_data(url):
    # Check if the cache file already there
    if os.path.isfile(path_to_urlScan_Cache+url+'.json') == 1:
        # if the file is there call the grab cache data function
        urlScan_file = urlScan_file_getData(url)
        # Return the results from the cache file
        return urlScan_file
    # If the cache file doesn't showup call the API
    else:
        # Call the api function with the url
        urlScan_api = urlscan_URL_GetData(url)
        # Check if the api call was successful
        if urlScan_api.status_code == 200:

            # Get the response to look nicer
            decodedResponse = json.loads(urlScan_api.text)
            urlScan_formatted = json.dumps(decodedResponse, sort_keys=True, indent=4)

            # fx = file create
            # create the file with the ip.json
            fx = open(path_to_urlScan_Cache+url+".json", 'x')
            # write the data from the api request to the new file
            fx.write(urlScan_formatted)
            # close the created file
            fx.close()
            # Check if the file was successfully created
            if os.path.isfile(path_to_urlScan_Cache+url+'.json') == 1:
                # fr = file read
                # Read the newly made file
                fr = open(path_to_urlScan_Cache+url+".json", 'r')
                # load the json values
                data = fr.read()
                # close the file
                fr.close()
                return data
            else:
                return 1
        elif urlScan_api.status_code == 400:
            return 2
        elif urlScan_api.status_code == 404:
            return 3
        else:
            return 4


# Call the urlscan get data function with the data given by the user
print("Please note: urls are scanned publicly")
url = input("Enter The URL :: ")
url_request = urlScan_xr_data(url)
print(url_request)