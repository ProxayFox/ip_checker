# Testing URLScan
import validators
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

def urlScan_file_saveData(urlScan_api):
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

def urlScan_xr_data(url):
    # IP Validator request
    v_url = not validators.url(url)
    # v_url = False
    # If IP is valid validator will return False - I know this sounds dumb but trust me
    if v_url == False:
        # Check if the cache file already there
        if os.path.isfile(path_to_urlScan_Cache+url+'.json') == 1:
            # with the cache already being there, get the data
            urlScan_file = urlScan_file_getData(url)
            # Return the results from the cache file
            return urlScan_file
        # If the cache file doesn't showup call the API
        else:
            # Call the api function with the url
            urlScan_api = urlscan_URL_GetData(url)
            # Check if the api call was successful
            if urlScan_api.status_code == 200:
                # Pass the file to be saved in cache
                urlScan_file_saveData(urlScan_api)

                # Now that the file should be made, call it
                # TODO :: Maybe find a better way or trust it's there so the data passer can be faster
                if os.path.isfile(path_to_urlScan_Cache+url+'.json') == 1:
                    
                    # After the file has been created and checked all is well grab that data
                    data = urlScan_file_getData(v_url)
                    return data
                else:
                    return "URLScan :: File not created for Value :: "+url
            elif urlScan_api.status_code == 400:
                return "URLScan :: Not Found or Missing Value for Value :: "+url
            elif urlScan_api.status_code == 404:
                return "URLScan :: No Response for Value :: "+url
            else:
                return "URLScan :: Something is missing for Value :: "+url
    # If IP is valid validator will return True - I know this sounds dumb but trust me
    elif v_url == True:
        return "URLScan :: Invalid URL address for value :: "+url
    # Something has gone wrong don't know what would cause this xD
    else:
        return "URLScan :: You Broke something :D"


# Call the urlscan get data function with the data given by the user
print("Please note: urls are scanned publicly")
url = input("Enter The URL :: ")
url_request = urlScan_xr_data(url)
print(url_request)