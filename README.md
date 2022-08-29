# IP Checker/Information Grabbing

## how to run as of 29/08/2022
In the terminal or you method of running py run:
<br>
`py main.py`
<br>
It will ask you to enter the address to search
```bash
Enter The Ip ::
```
Enter the address, and so far it'll show
```bash
PS C:\path\to\working\dir> py .\main.py
Enter The Ip :: 1.1.1.1
Results From VT for 1.1.1.1
AS Owner :: CLOUDFLARENET No. 13335
harmless :: 80
malicious :: 4
suspicious :: 0
undetected :: 10
Results From ABIP for 1.1.1.1
ISP :: APNIC and CloudFlare DNS Resolver Project
Usage Type :: Content Delivery Network
Country Name :: United States of America        
AbuseIP Confidence Score :: 0
Total Reports :: 25
```

# Create New file called api_secrets.json with the following
```json
{
    "api": {
        "vt_key":   "Enter VirusTotal Key",
        "urlScan_key": "Enter urlScan Key",
        "abuseIP_key": "Enter abuseIP key",
        "otx_Key": "Enter OTX Key"
    }
}
```
Put the file in home dir of the app

## Grabb the Keys
all the apis are free to use with limitations on amount of requests

## TODO list for more information
To be updated as I go