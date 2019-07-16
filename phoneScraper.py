"""This module downloads html page, finds Russian phone numbers
and returns them as a set of phone numbers in 8KKKNNNNNNN format"""

import re
import urllib.request

regex = r'(?<![.\d])([+]?[7|9|8][ ]?[(]?[4|2|6|5|7|8|9|0]{3}[)]?[ ]?\d{2,3}[- ]?\d{2}[- ]?\d{2})'
pattern = re.compile(regex)


def reformat(string: str):
    """Returns phone number converted to 8KKKNNNNNNN format"""
    string = string.replace('-', ''). \
        replace('(', ''). \
        replace(')', ''). \
        replace(' ', ''). \
        replace('+7', '8')
    return string


def get_phone_number(url: str):
    """Returns a set of phone numbers in 8KKKNNNNNNN format"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/6.0'})  # prevents mod_security's HTTP 403
    with urllib.request.urlopen(req) as response:
        page = response.read()
        phones = set(re.findall(pattern, str(page)))
        phones = set(map(reformat, phones))
    return phones
