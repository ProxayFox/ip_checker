import ipaddress

# IP validator
def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return 1
    except ValueError:
        return 0

# TODO: URL Validator

# TODO: Hash Validator

# TODO: Email Validator