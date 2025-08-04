import yaml
import os
import validators
import ipaddress
import sys

# Import Internal Functions
import virusTotal
import abipdb

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "conf.yaml")

SAMPLE_CONFIG = {
  "api": {
    "vt_key": "Enter VirusTotal Key",
    "urlScan_key": "Enter urlScan Key",
    "abuseIP_key": "Enter abuseIP key"
  },
  "cache": {
    "holding_days": 60
  }
}

def create_sample_config(path):
  with open(path, "w") as f:
    yaml.dump(SAMPLE_CONFIG, f, default_flow_style=False)
  print(f"\nSample configuration file created at: {path}")
  print("Please edit this file and add your API keys before running the script again.\n")

def load_config(path):
  if not os.path.exists(path):
    create_sample_config(path)
    sys.exit(1)
  with open(path, "r") as f:
    config = yaml.safe_load(f)
  return config

def validate_config(config):
  required_api_keys = ["vt_key", "urlScan_key", "abuseIP_key"]
  if "api" not in config or not isinstance(config["api"], dict):
    raise ValueError("Missing or invalid 'api' section in config.")
  for key in required_api_keys:
    if key not in config["api"] or not isinstance(config["api"][key], str) or not config["api"][key]:
      raise ValueError(f"Missing or invalid API key: {key}")
  if "cache" not in config or not isinstance(config["cache"], dict):
    raise ValueError("Missing or invalid 'cache' section in config.")
  if "holding_days" not in config["cache"] or not isinstance(config["cache"]["holding_days"], int):
    raise ValueError("Missing or invalid 'holding_days' in cache config.")

def main():
  # Load and validate config
  try:
    config = load_config(CONFIG_PATH)
    validate_config(config)
  except Exception as e:
    print(f"Config error: {e}")
    sys.exit(1)

  # Get the data from the user for IPs
  grab_ip = input("Enter The IP/s :: ")
  split_ip = grab_ip.split(' ')

  for ip in split_ip:
    v_ip = not validators.ip_address.ipv4(ip)
    privOrPub_ip = ipaddress.ip_address(ip).is_private
    if not privOrPub_ip:
      if not v_ip:
        vt = virusTotal.vt_xr_data(ip, config["api"]["vt_key"], config["cache"]["holding_days"])
        if isinstance(vt, dict):
          print("Results From VT for", ip)
          try:
            print("AS Owner ::", vt['data']['attributes']['as_owner'], "No.", vt['data']['attributes']['asn'])
          except:
            print("AS Owner :: Missing :: No. Missing")
          print("harmless ::", vt['data']['attributes']['last_analysis_stats']['harmless'])
          print("malicious ::", vt['data']['attributes']['last_analysis_stats']['malicious'])
          print("suspicious ::", vt['data']['attributes']['last_analysis_stats']['suspicious'])
          print("Com Vote Harmless :: ", vt['data']['attributes']['total_votes']['harmless'])
          print("Com Vote Malicious :: ", vt['data']['attributes']['total_votes']['malicious'])
        elif isinstance(vt, str):
          print(vt)
        else:
          print(vt)
        abip = abipdb.abip_xr_data(ip, config["api"]["abuseIP_key"], config["cache"]["holding_days"])
        if isinstance(abip, dict):
          print("Results From ABIP for", ip)
          print("ISP ::", abip['data']['isp'])
          print("Usage Type ::", abip['data']['usageType'])
          print("Country Name ::", abip['data']['countryName'])
          print("AbuseIP Confidence Score ::", abip['data']['abuseConfidenceScore'])
          print("Total User Reports ::", abip['data']['totalReports'])
          print("")
        elif isinstance(abip, str):
          print(abip)
        else:
          print("ABIP :: Something has gone wrong")
      else:
        print("Invalid IP address for value :: "+ip)
        print("")
    elif privOrPub_ip:
      print("Private IP Address :: "+ip)
      print("")
    else:
      print("You Broke something :D")

if __name__ == "__main__":
  main()
