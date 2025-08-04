# IP Checker/Information Grabbing

## How to Run
In the terminal or you method of running py run:
<br>
``` bash
  python main.py
```
<br>
It will ask you to enter the address to search
``` txt
  Enter The Ip ::
```
Enter the address, and you'll see
``` txt
  PS C:\path\to\working\dir> py .\main.py
  Enter The IP/s :: 1.1.1.1
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

## How to bulk search for IPs
Separate each ip with a space such like bellow to search for multiple IP
<br>
``` txt
  Enter The IP/s :: 1.1.1.1 1.0.0.1 8.8.8.8
```



# Setup the Config
By running `python main.py` it will create a template conf.yaml file for you to enter the keys into
``` yaml
api:
  abuseIP_key: Enter abuseIP key
  urlScan_key: Enter urlScan Key
  vt_key: Enter VirusTotal Key
cache:
  holding_days: 60
```
### API
this will contain all the keys

### Cache
This is the amount of time you want to store API Cached requests before getting a new value


## Grab the Keys
all the apis are free to use with limitations on amount of requests

## Python packages required
``` bash
pip install -r requirements.txt
```
