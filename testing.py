# Import Python libraries  
import validators

# Import Internal Functions
import virusTotal
import abipdb

# Get the data from the user for IPs
grab_ip = input("Enter The IP/s :: ")
# Creates a string separating the IPs at space
split_ip = grab_ip.split(' ')

# TODO: Move to callable function
# Loop through IPs will also work with one address
for ip in split_ip :
    # IP Validator request
    v_ip = not validators.ip_address.ipv4(ip)
    # If IP is valid validator will return False - I know this sounds dumb but trust me
    if v_ip == False:
        # Call VT Checker
        vt = virusTotal.vt_xr_data(ip)
        # Error Handler
        # Check if returned value is a dictionary
        if type(vt) is dict:
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
        # Check if returned value is a string and print it
        elif type(vt) is str:
            print(vt)
        # I'm not sure what would get to this point but something has gone wrong
        else: 
            print("VTIP :: Something has gone wrong")

        # Call ABIP Checker
        abip = abipdb.abip_xr_data(ip)
        # Error Handler
        # Check if returned value is a dictionary
        if type(abip) is dict:
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
            print("Total User Reports ::", data_totalReports)
            print("")
        # Check if returned value is a string and print it
        elif type(abip) is str:
            print(abip)
        # I'm not sure what would get to this point but something has gone wrong
        else: 
            print("ABIP :: Something has gone wrong")

    # If IP is valid validator will return True - I know this sounds dumb but trust me
    elif v_ip == True:
        print("Invalid IP address for value :: "+ip)
        print("")
    # Something has gone wrong don't know what would cause this xD
    else:
        print("You Broke something :D")