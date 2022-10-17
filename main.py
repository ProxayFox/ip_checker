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
    # If IP is valid validator will return False - This confuses me too
    if v_ip == False:
        # Call VT Checker
        vt = virusTotal.vt_xr_data(ip)
        # Error Handler
        # Check if returned value is a dictionary
        if type(vt) is dict:
            print("Results From VT for", ip)
            try:
                print("AS Owner ::", vt['data']['attributes']['as_owner'], "No.", vt['data']['attributes']['asn'])
            except:
                print("AS Owner :: Missing :: No. Missing")
            print("harmless ::", vt['data']['attributes']['last_analysis_stats']['harmless'])
            print("malicious ::", vt['data']['attributes']['last_analysis_stats']['malicious'])
            print("suspicious ::", vt['data']['attributes']['last_analysis_stats']['suspicious'])
            # print("undetected ::", vt['data']['attributes']['last_analysis_stats']['undetected'])
            # print("VT Community")
            print("Com Vote Harmless :: ", vt['data']['attributes']['total_votes']['harmless'])
            print("Com Vote Malicious :: ", vt['data']['attributes']['total_votes']['malicious'])
        # Check if returned value is a string and print it
        elif type(vt) is str:
            print(vt)
        # I'm not sure what would get to this point but something has gone wrong
        else: 
            print(vt)

        # Call ABIP Checker
        abip = abipdb.abip_xr_data(ip)
        # Error Handler
        # Check if returned value is a dictionary
        if type(abip) is dict:
            print("Results From ABIP for", ip)
            print("ISP ::", abip['data']['isp'])
            print("Usage Type ::", abip['data']['usageType'])
            print("Country Name ::", abip['data']['countryName'])
            print("AbuseIP Confidence Score ::", abip['data']['abuseConfidenceScore'])
            print("Total User Reports ::", abip['data']['totalReports'])
            print("")
        # Check if returned value is a string and print it
        elif type(abip) is str:
            print(abip)
        # I'm not sure what would get to this point but something has gone wrong
        else: 
            print("ABIP :: Something has gone wrong")

    # If IP is valid validator will return True - This confuses me too
    elif v_ip == True:
        print("Invalid IP address for value :: "+ip)
        print("")
    # Something has gone wrong don't know what would cause this xD
    else:
        print("You Broke something :D")