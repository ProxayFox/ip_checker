import requests
import json
import os

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')
# Get the current working directory directory
cwd = os.getcwd()

# Grab the VT Cache directory
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
            abip_api_formated = json.dumps(decodedResponse, sort_keys=True, indent=4)

            # fx = file create
            # creat the file with the ip.json
            fx = open(path_to_abipCache+ip+".json", 'x')
            # write the data from the api request to the new file
            fx.write(abip_api_formated)
            # close the created file
            fx.close()
            # Check if the file was succesfully created
            if os.path.isfile(path_to_abipCache+ip+'.json') == 1:
                # print("New Cache file has been made")
                # fr = file read
                # Read the newly made file
                fr = open(path_to_abipCache+ip+".json", 'r')
                # load the json valuse
                data = fr.read()
                # print(ip, "::" , data['data']['attributes']['last_analysis_stats'])
                # close the file
                fr.close()
                return json.loads(data)
            else:
                # print("File not created")
                return 1
        elif abip_api.status_code == 400:
            # print('Not Found or Missing Value.')
            return 2
        elif abip_api.status_code == 404:
            # print('No Response.')
            return 3
        else:
            # print("Something is missing")
            return 4

ip = input("Enter The Ip :: ")
abip = abip_xr_data(ip)
if abip == 1:
    print("File not created")
elif abip == 2:
    print('Not Found or Missing Value.')
elif abip == 3:
    print('No Response.')
elif abip == 4:
    print("Something is missing")
else:
    data_isp = abip['data']['isp']
    data_usageType = abip['data']['usageType']
    data_countryName = abip['data']['countryName']
    data_abuseConfidenceScore = abip['data']['abuseConfidenceScore']
    data_totalReports = abip['data']['totalReports']
    print("Results for", ip)
    print("ISP ::", data_isp)
    print("Usage Type ::", data_usageType)
    print("Country Name ::", data_countryName)
    print("AbuseIP Confidence Score ::", data_abuseConfidenceScore)
    print("Total Reports ::", data_totalReports)


# ip = input("Enter The Ip :: ")
# abip = abip_url_getData(ip)
# print(abip.status_code)