import requests
import json
import os
import time
import fnmatch

# set working directory (windows)
# os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the VT Cache directory
path_to_vtCache = cwd+"\\DataDumps\\virusTotal\\"

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
def vtFileGetData(fileName):
    # fr = file read
    # Open File and read the details
    fr = open(path_to_vtCache+fileName,'r')
    # Read the content and load the json
    data = json.loads(fr.read())
    # Close the file
    fr.close()
    return data

# Get the name of the file
def getFileName(ip):
    filterOn = ip+"*.json"
    dirList = os.listdir(path_to_vtCache)
    findFile = fnmatch.filter(dirList, filterOn)
    return findFile

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

# Function checks if the file is exists or is valid
def checkIfFileExists(ip):
    fileName = getFileName(ip)
    if len(fileName) == 1:
        if os.path.exists(path_to_vtCache+fileName[0]) == True:
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
        vt_api = vt_url_getData(ip)
        if vt_api.status_code == 200:
            # fx = file create
            # create the file with the ip.json
            fx = open(path_to_vtCache+ip+'_'+str(int(time.time()))+".json", 'x')
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
    os.remove(str(path_to_vtCache+getFileName(ip)[0]))
    # time.sleep(0.5)
    if checkIfFileExists(ip)[0] == 0:
        # File has been deleted
        return 1
    else:
        # File is still there
        return 0

# Function to handle VirusTotal API/File requests
def vt_xr_data(ip):
    # Check if the file exists
    if checkIfFileExists(ip)[0] == 1:
        if getTimeDif(ip)[0] == 1:
            # call function to get the file
            return vtFileGetData(getFileName(ip)[0])
        else:
            delete = deleteFile(ip)
            makeFile  = createFile(ip)

            if delete == 1:
                if makeFile[0]  == 1:
                    return vtFileGetData(getFileName(ip)[0])
                else:
                    return makeFile
    else:
        makeFile  = createFile(ip)
        if makeFile[0]  == 1:
            return vtFileGetData(getFileName(ip)[0])
        else:
            return makeFile

print(path_to_vtCache)