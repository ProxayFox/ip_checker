import requests
import json
import os

def vt_url_getData(ip):
    # Get the API Secret
    # fr = File Read
    fr = open('api_secrets.json', 'r')
    # gss = Google Safe Search
    gss_key = json.loads(fr.read())['api']['google']
    # close the 
    fr.close()
    # Defining the api-endpoint with the address on the end
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key="+gss_key
    
    headers = {
        "Accept": "application/json"
    }
    
    # return data to the request
    return requests.get(url, headers=headers)