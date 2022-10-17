import os
import fnmatch
import json
import time

# set working directory (windows)
os.chdir(os.getcwd())
# Get the current working directory directory
cwd = os.getcwd()
# Grab the VT Cache directory
path_to_vtCache = cwd+"/DataDumps/virusTotal"

ip = '1.1.1.1'
# currentTime = int(time.time())

test= path_to_vtCache+ip+'_'+str(int(time.time()))+".json"
print(test)





