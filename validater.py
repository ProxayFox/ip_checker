import ipaddress 

def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return 1
    except ValueError:
        return 0

ip = validate_ip_address(input("Enter The IP/s :: "))

if ip == 1:
    print("good")
elif ip == 0:
    print("bad")