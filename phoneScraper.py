"""This module downloads html page, finds Russian phone numbers
and returns them as a set of phone numbers in 8KKKNNNNNNN format"""

import re
from urllib import request, error

regex: str = r'(?<![.\d])([+]?[7|9|8][ ]?[(]?[4|2|6|5|7|8|9|0]{3}[)]?[ ]?\d{2,3}[- ]?\d{2}[- ]?\d{2})'
reform_regex_bkt: str = r' |\(|\)|-'
reform_regex_code: str = r'[+]?[7]'
pattern = re.compile(regex)
reform_pattern_bkt = re.compile(reform_regex_bkt)
reform_pattern_code = re.compile(reform_regex_code)


def get_phone_number(url: str) -> set:
    """Returns a set of phone numbers in 8KKKNNNNNNN format"""
    req = request.Request(url, headers={'User-Agent': 'Mozilla/6.0'})  # prevents mod_security's HTTP 403
    try:
        with request.urlopen(req) as response:
            print('response: ', response.getcode())
            page = response.read()
            phones = pattern.findall(str(page))
            phones = [re.sub(reform_pattern_bkt, '', s) for s in phones]
            phones = set([re.sub(reform_regex_code, '8', s) for s in phones])
    except error.HTTPError as err:
        if err.code == 404:
            return {}
    return phones
