#!/usr/bin/env python3
# <editor-fold desc='Imports'>

from getpass import getpass
import hashlib
import re
import requests
import sys

# </editor-fold>


# <editor-fold desc='Globals'>

# The api url of pwnedpasswords.com
URL = 'https://api.pwnedpasswords.com/range/'
# The number of characters to pass to the api
PREFIX_LEN = 5

# </editor-fold>


def process_response(response, hash_suffix):
    # Use regular expressions to determine if the hashes match
    pattern = re.compile(f'^{hash_suffix}', re.I)
    # Split response into lines
    for item in response.text.splitlines():
        # Check for the item with a matching hash suffix
        if pattern.match(item):
            return item
    # Item with matching hash suffix not found
    return None


def main():
    # Get the password from the user
    password = getpass('Password to check: ')
    # Hash the password with sha1
    hash = hashlib.sha1(str.encode(password)).hexdigest()

    # Query the api for the hash prefix
    response = requests.get(f'{URL}{hash[:PREFIX_LEN]}')
    # Make sure the api returned status OK
    if response.status_code != 200:
        print(f'request error\n{URL} returned {response.status_code}')
        sys.exit()
    # Process the api response
    item = process_response(response, hash[PREFIX_LEN:])

    # Print information to user
    print(f'Hash = {hash}')
    if item:
        print(f'Password has been leaked {item.split(":")[-1]} times according to the https://haveibeenpwned.com/ Pwned Passwords API')
    else:
        print(f'Password has not been leaked according to the https://haveibeenpwned.com/ Pwned Passwords API')


if __name__ == '__main__':
    main()
