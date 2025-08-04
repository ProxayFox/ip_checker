import requests
import json
import os
import time
import fnmatch

cwd = os.getcwd()
path_to_abipCache = cwd + "/DataDumps/abuseIP/"

def abip_url_getData(ip, abip_key):
  url = 'https://api.abuseipdb.com/api/v2/check'
  querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '90',
    'verbose': 'true'
  }
  headers = {
    'Accept': 'application/json',
    'Key': abip_key
  }
  return requests.get(url, headers=headers, params=querystring)

def abipFileGetData(fileName):
  with open(path_to_abipCache + fileName, 'r') as fr:
    data = json.load(fr)
  return data

def getFileName(ip):
  filterOn = ip + "*.json"
  dirList = os.listdir(path_to_abipCache)
  findFile = fnmatch.filter(dirList, filterOn)
  return findFile

def getTimeDif(ip, holding_days):
  fileName = getFileName(ip)
  if not fileName:
    return (0, None, None)
  removeIP = fileName[0].split('_')
  removeJson = removeIP[1].split('.json')
  fileTime = int(removeJson[0])
  currentTime = int(time.time())
  getDif = (currentTime - fileTime) / 86400
  if holding_days > getDif:
    return (1, fileName[0], getDif)
  else:
    return (0, fileName[0], getDif)

def checkIfFileExists(ip):
  fileName = getFileName(ip)
  if len(fileName) == 1:
    if os.path.exists(path_to_abipCache + fileName[0]):
      return (1, fileName[0], "valid path")
    else:
      return (0, fileName[0], "no path")
  else:
    if len(fileName) == 0:
      return (0, fileName, "No file")
    elif len(fileName) >= 2:
      return (0, fileName, "too many of same file")
    else:
      return (0, fileName, "error")

def createFile(ip, abip_key):
  if checkIfFileExists(ip)[0] == 0:
    abip_api = abip_url_getData(ip, abip_key)
    if abip_api.status_code == 200:
      fx = open(path_to_abipCache + ip + '_' + str(int(time.time())) + ".json", 'x')
      fx.write(abip_api.text)
      fx.close()
      isfile = checkIfFileExists(ip)
      if isfile[0] == 1:
        return (1, "File Creation Successful", isfile)
      else:
        return (0, "File Creation Unsuccessful", isfile)
    elif abip_api.status_code == 400:
      return (0, f"ABIP :: Not Found or Missing Value for Value :: {ip} :: Status Code :: {abip_api.status_code}")
    elif abip_api.status_code == 404:
      return (0, f"ABIP :: No Response for Value :: {ip} :: Status Code :: {abip_api.status_code}")
    else:
      return (0, f"ABIP :: Server Error :: {ip} :: Status Code :: {abip_api.status_code} :: Or API Keys are missing")
  else:
    return (0, checkIfFileExists(ip))

def deleteFile(ip):
  os.remove(str(path_to_abipCache + getFileName(ip)[0]))
  if checkIfFileExists(ip)[0] == 0:
    return 1
  else:
    return 0

def abip_xr_data(ip, abip_key, holding_days):
  if checkIfFileExists(ip)[0] == 1:
    if getTimeDif(ip, holding_days)[0] == 1:
      return abipFileGetData(getFileName(ip)[0])
    else:
      delete = deleteFile(ip)
      makeFile = createFile(ip, abip_key)
      if delete == 1:
        if makeFile[0] == 1:
          return abipFileGetData(getFileName(ip)[0])
        else:
          return makeFile
  else:
    makeFile = createFile(ip, abip_key)
    if makeFile[0] == 1:
      return abipFileGetData(getFileName(ip)[0])
    else:
      return makeFile
