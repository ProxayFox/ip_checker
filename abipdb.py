import requests
import json
import os
import time
import fnmatch

# set working directory (windows)
# os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the ABIP Cache directory
path_to_abipCache = cwd+"\\DataDumps\\abuseIP\\"

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
def abipFileGetData(fileName):
    # file = open(path_to_abipCache+ip+'.json','r')
    # data = json.loads(file.read())
    # file.close()
    # return data

    # fr = file read
    # Open File and read the details
    fr = open(path_to_abipCache+fileName,'r')
    # Read the content and load the json
    data = json.loads(fr.read())
    # Close the file
    fr.close()
    return data


# Function to get the time difference in current time and file time
def getTimeDif (ip):
    fileName = getFileName(ip)
    removeIP = fileName[0].split('_')
    removeJson = removeIP[1].split('.json')
    fileTime = int(removeJson[0])
    currentTime = int(time.time())
    getDif = (currentTime - fileTime) / 86400

    file = open("conf.json",'r')
    cacheLength = int(json.loads(file.read())['cache']['holding_days'])
    file.close()

    if cacheLength > getDif:
        # Cache Time difference is within config
        return (1, fileName[0], getDif)
    else:
        # Cache Time difference is outside config
        return (0, fileName[0], getDif)

# Get the name of the file
def getFileName(ip):
    filterOn = ip+"*.json"
    dirList = os.listdir(path_to_abipCache)
    findFile = fnmatch.filter(dirList, filterOn)
    return findFile

# Function checks if the file is exists or is valid
def checkIfFileExists(ip):
    fileName = getFileName(ip)
    if len(fileName) == 1:
        if os.path.exists(path_to_abipCache+fileName[0]) == True:
            # return 1 if there is a file
            return (1, fileName[0], "valid path")
        else:
            # return 0 if there is no file
            return (0, fileName[0], "no path")
    else:
        if len(fileName) == 0:
            # return 0 if the file doesn't exists
            return (0, fileName, "No file")
        elif len(fileName) >= 2:
            return (0, fileName, "too many of same file")
        else:
            return (0, fileName, "error")
    # return len(fileName)

# Create file 
def createFile(ip):
    if checkIfFileExists(ip)[0] == 0:
        vt_api = abip_url_getData(ip)
        if vt_api.status_code == 200:
            # fx = file create
            # create the file with the ip.json
            fx = open(path_to_abipCache+ip+'_'+str(int(time.time()))+".json", 'x')
            # write the data from the api request to the new file
            fx.write(vt_api.text)
            # close the created file
            fx.close()
            # Check if the file was successfully created
            isfile = checkIfFileExists(ip)
            if isfile[0] == 1:
                # File has been successfully created
                return (1, "File Creation Successful", isfile)
            else:
                # File has been unsuccessfully created
                return (0, "File Creation Unsuccessful", isfile)
        elif vt_api.status_code == 400:
            return (0, "VTIP :: Not Found or Missing Value for Value :: "+ip+" :: Status Code :: "+vt_api.status_code)

        elif vt_api.status_code == 404:
            return (0, "VTIP :: No Response for Value :: "+ip+" :: Status Code :: "+vt_api.status_code)

        else:
            return (0, "VTIP :: Server Error :: "+ip+" :: Status Code :: "+vt_api.status_code)
    else:
        return (0, checkIfFileExists(ip))

def deleteFile(ip):
    os.remove(str(path_to_abipCache+getFileName(ip)[0]))
    # time.sleep(0.5)
    if checkIfFileExists(ip)[0] == 0:
        # File has been deleted
        return 1
    else:
        # File is still there
        return 0

# Function to handle VirusTotal API/File requests
def abip_xr_data(ip):
    # Check if the file exists
    if checkIfFileExists(ip)[0] == 1:
        if getTimeDif(ip)[0] == 1:
            # call function to get the file
            return abipFileGetData(getFileName(ip)[0])
        else:
            delete = deleteFile(ip)
            makeFile  = createFile(ip)

            if delete == 1:
                if makeFile[0]  == 1:
                    return abipFileGetData(getFileName(ip)[0])
                else:
                    return makeFile
    else:
        makeFile  = createFile(ip)
        if makeFile[0]  == 1:
            return abipFileGetData(getFileName(ip)[0])
        else:
            return makeFile


print(path_to_abipCache)




















# def abip_xr_data(ip):
#     # Check if the file exists
#     if os.path.isfile(path_to_abipCache+ip+'.json') == 1:
#         abip_file = abip_file_getData(ip)
#         return abip_file

#     else:
#         abip_api = abip_url_getData(ip)
#         if abip_api.status_code == 200:
#             # format the returned results
#             decodedResponse = json.loads(abip_api.text)
#             abip_api_formatted = json.dumps(decodedResponse, sort_keys=True, indent=4)

#             # fx = file create
#             # create the file with the ip.json
#             fx = open(path_to_abipCache+ip+".json", 'x')
#             # write the data from the api request to the new file
#             fx.write(abip_api_formatted)
#             # close the created file
#             fx.close()
#             # Check if the file was successfully created
#             if os.path.isfile(path_to_abipCache+ip+'.json') == 1:
#                 # fr = file read
#                 # Read the newly made file
#                 fr = open(path_to_abipCache+ip+".json", 'r')
#                 # load the json values
#                 data = fr.read()
#                 # close the file
#                 fr.close()
#                 return json.loads(data)
#             else:
#                 return "ABIP :: File not created for Value :: "+ip
#                 # return 1
#         elif abip_api.status_code == 400:
#             return "ABIP :: Not Found or Missing Value for Value :: "+ip
#             # return 2
#         elif abip_api.status_code == 404:
#             return "ABIP :: No Response for Value :: "+ip
#             # return 3
#         else:
#             return "ABIP :: Something is missing for Value :: "+ip
#             # return 4