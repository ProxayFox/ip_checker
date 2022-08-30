import requests
import json
import os

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')
# Get the current working directory directory
cwd = os.getcwd()
# Grab the VT Cache directory
path_to_vtCache = cwd+"/DataDumps/virusTotal/"

# Function to reqeust data from Virus total
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
        # print("File is there")
        # call function to get the file
        vt_file = vt_file_getData(ip)
        # print(ip, "::" , vt_file['data']['attributes']['last_analysis_stats'])
        return vt_file
    # if the file isn't there do an api call to get data and make file
    else:
        # call the cunctation that handles the api request to VT
        vt_api = vt_url_getData(ip)
        # print(vt_api.status_code)
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
                # print("New Cache file has been made")
                # fr = file read
                # Read the newly made file
                fr = open(path_to_vtCache+ip+".json", 'r')
                # load the json values
                data = json.loads(fr.read())
                # print(ip, "::" , data['data']['attributes']['last_analysis_stats'])
                # close the file
                fr.close()
                return data
            else:
                # print("File not created")
                return 1
        elif vt_api.status_code == 400:
            # print('Not Found or Missing Value.')
            return 2
        elif vt_api.status_code == 404:
            # print('No Response.')
            return 3
        else:
            # print("Something is missing")
            return 4


# ip = input("Enter The Ip :: ")
# # Grab the VT Cache directory
# path_to_vtCache = cwd+"/DataDumps/virusTotal/"
# vt = vt_xr_data(ip)
# if vt == 1:
#     print("File not created")
# elif vt == 2:
#     print('Not Found or Missing Value.')
# elif vt == 3:
#     print('No Response.')
# elif vt == 4:
#     print("Something is missing")
# else:
#     data_attributes_lastAnalysisStats_harmless = vt['data']['attributes']['last_analysis_stats']['harmless']
#     data_attributes_lastAnalysisStats_malicious = vt['data']['attributes']['last_analysis_stats']['malicious']
#     data_attributes_lastAnalysisStats_suspicious = vt['data']['attributes']['last_analysis_stats']['suspicious']
#     data_attributes_lastAnalysisStats_undetected = vt['data']['attributes']['last_analysis_stats']['undetected']
#     data_attributes_asOwner = vt['data']['attributes']['as_owner']
#     data_attributes_asn = vt['data']['attributes']['asn']
#     print("Results for", ip)
#     print("AS Owner ::", data_attributes_asOwner, "No.", data_attributes_asn)
#     print("harmless ::", data_attributes_lastAnalysisStats_harmless)
#     print("malicious ::", data_attributes_lastAnalysisStats_malicious)
#     print("suspicious ::", data_attributes_lastAnalysisStats_suspicious)
#     print("undetected ::", data_attributes_lastAnalysisStats_undetected)