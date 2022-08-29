import requests
import json
import os
import vt_ip_score
import abip_ip_score

# set working directory (windows)
os.chdir(r'C:\xampp\htdocs\Python\IP_Validate')
# Get the current working directory directory
cwd = os.getcwd()

ip = input("Enter The Ip :: ")
# Grab the VT Cache directory
# path_to_vtCache = cwd+"/DataDumps/virusTotal/"


vt = vt_ip_score.vt_xr_data(ip)
if vt == 1:
    print("File not created")
elif vt == 2:
    print('Not Found or Missing Value.')
elif vt == 3:
    print('No Response.')
elif vt == 4:
    print("Something is missing")
else:
    data_attributes_lastAnalysisStats_harmless = vt['data']['attributes']['last_analysis_stats']['harmless']
    data_attributes_lastAnalysisStats_malicious = vt['data']['attributes']['last_analysis_stats']['malicious']
    data_attributes_lastAnalysisStats_suspicious = vt['data']['attributes']['last_analysis_stats']['suspicious']
    data_attributes_lastAnalysisStats_undetected = vt['data']['attributes']['last_analysis_stats']['undetected']
    data_attributes_asOwner = vt['data']['attributes']['as_owner']
    data_attributes_asn = vt['data']['attributes']['asn']
    print("Results From VT for", ip)
    print("AS Owner ::", data_attributes_asOwner, "No.", data_attributes_asn)
    print("harmless ::", data_attributes_lastAnalysisStats_harmless)
    print("malicious ::", data_attributes_lastAnalysisStats_malicious)
    print("suspicious ::", data_attributes_lastAnalysisStats_suspicious)
    print("undetected ::", data_attributes_lastAnalysisStats_undetected)
    
# ip = input("Enter The Ip :: ")
abip = abip_ip_score.abip_xr_data(ip)
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
    print("Results From ABIP for", ip)
    print("ISP ::", data_isp)
    print("Usage Type ::", data_usageType)
    print("Country Name ::", data_countryName)
    print("AbuseIP Confidence Score ::", data_abuseConfidenceScore)
    print("Total Reports ::", data_totalReports)
    exit()