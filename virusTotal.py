import requests
import json
import os
import time
import fnmatch

cwd = os.getcwd()
path_to_vtCache = cwd+"/DataDumps/virusTotal/"

def vt_url_getData(ip, vt_key):
  url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
  headers = {
    "Accept": "application/json",
    "x-apikey": vt_key
  }
  return requests.get(url, headers=headers)

def vtFileGetData(fileName):
  with open(path_to_vtCache+fileName, 'r') as fr:
    data = json.load(fr)
  return data

def getFileName(ip):
  filterOn = ip+"*.json"
  dirList = os.listdir(path_to_vtCache)
  findFile = fnmatch.filter(dirList, filterOn)
  return findFile

def getTimeDif(ip, holding_days):
  fileName = getFileName(ip)
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
    if os.path.exists(path_to_vtCache+fileName[0]):
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

def createFile(ip, vt_key):
  if checkIfFileExists(ip)[0] == 0:
    vt_api = vt_url_getData(ip, vt_key)
    if vt_api.status_code == 200:
      fx = open(path_to_vtCache + ip + '_' + str(int(time.time())) + ".json", 'x')
      fx.write(vt_api.text)
      fx.close()
      isfile = checkIfFileExists(ip)
      if isfile[0] == 1:
        return (1, "File Creation Successful", isfile)
      else:
        return (0, "File Creation Unsuccessful", isfile)
    elif vt_api.status_code == 400:
      return (0, f"VTIP :: Not Found or Missing Value for Value :: {ip} :: Status Code :: {vt_api.status_code}")
    elif vt_api.status_code == 404:
      return (0, f"VTIP :: No Response for Value :: {ip} :: Status Code :: {vt_api.status_code}")
    else:
      return (0, f"VTIP :: Server Error :: {ip} :: Status Code :: {vt_api.status_code} :: Or API Keys are missing")
  else:
    return (0, checkIfFileExists(ip))

def deleteFile(ip):
  os.remove(str(path_to_vtCache+getFileName(ip)[0]))
  if checkIfFileExists(ip)[0] == 0:
    return 1
  else:
    return 0

def vt_xr_data(ip, vt_key, holding_days):
  if checkIfFileExists(ip)[0] == 1:
    if getTimeDif(ip, holding_days)[0] == 1:
      return vtFileGetData(getFileName(ip)[0])
    else:
      delete = deleteFile(ip)
      makeFile  = createFile(ip, vt_key)
      if delete == 1:
        if makeFile[0]  == 1:
          return vtFileGetData(getFileName(ip)[0])
        else:
          return makeFile
  else:
    makeFile  = createFile(ip, vt_key)
    if makeFile[0]  == 1:
      return vtFileGetData(getFileName(ip)[0])
    else:
      return makeFile
