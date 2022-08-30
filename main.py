# Import Python libraries  

# Import Internal Functions
import vt_ip_score
import abip_ip_score
import validator

# Get the data from the user for IPs
grab_ip = input("Enter The IP/s :: ")
# Creates a string separating the IPs at space
split_ip = grab_ip.split(' ')

# TODO: Move to callable function
# Loop through IPs will also work with one address
for ip in split_ip :
    # IP Validator request
    v_ip = validator.validate_ip_address(ip)
    # If IP is valid validator will return 1
    if v_ip == 1:
        vt = vt_ip_score.vt_xr_data(ip)
        if vt == 1:
            print('VTIP :: File not created for Value :: '+ip)
        elif vt == 2:
            print('VTIP :: Not Found or Missing Value for Value :: '+ip)
        elif vt == 3:
            print('VTIP :: No Response for Value :: '+ip)
        elif vt == 4:
            print('VTIP :: Something is missing for Value :: '+ip)
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

        abip = abip_ip_score.abip_xr_data(ip)
        if abip == 1:
            print('ABIP :: File not created for Value :: '+ip)
            print("")
        elif vt == 2:
            print('ABIP :: Not Found or Missing Value for Value :: '+ip)
            print("")
        elif vt == 3:
            print('ABIP :: No Response for Value :: '+ip)
            print("")
        elif vt == 4:
            print('ABIP :: Something is missing for Value :: '+ip)
            print("")
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
            print("")
    # If IP is valid validator will return 0
    elif v_ip == 0:
        print("Invalid IP address for value :: "+ip)
        print("")
    # Something has gone wrong don't know what would cause this xD
    else:
        print("You Broke something :D")