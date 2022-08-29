import vt_ip_score
# 1.1.1.1 1.0.0.1 8.8.8.8
ip = input("Enter Bulk list :: ")
split_ip = ip.split(' ')

for ip in split_ip :
    vt = vt_ip_score.vt_xr_data(ip)
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