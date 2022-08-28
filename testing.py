# Testing how to read a fild
import requests
import json
import os

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')

def api_key():
    with open('api_secrets.txt', 'r') as file:
        vt = json.loads(file.read())
        return vt['api']['vt_key']

vt = api_key()
print(vt)