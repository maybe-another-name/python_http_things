import asyncio
from pyppeteer import connect

'''
Something copied in from burp, sent to pyppeteer.  Translates cookies to the pyppeteer format (unpacked list of dicts).
'''
import requests

burp0_url = "https://ac8d1f971e72893c813d090800110024.web-security-academy.net:443/my-account"
burp0_cookies = {"verify": "wiener", "session": "InVpbw2HmZY4PkWb83hgEwfSjlQ4tMUl"}
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://ac8d1f971e72893c813d090800110024.web-security-academy.net/login2", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)


def translate_burp_cookies_to_pyppeteer_cookies(burp_cookies) -> list:
  # https://miyakogi.github.io/pyppeteer/reference.html#page-class
  pyppeteer_cookies = []
  for key, value in burp_cookies.items():
    pyppeteer_cookie = {}
    pyppeteer_cookie.update({'url': burp0_url})
    pyppeteer_cookie.update({'name': key})
    pyppeteer_cookie.update({'value': value})
    pyppeteer_cookies.append(pyppeteer_cookie)
  return pyppeteer_cookies


async def main(url, cookies, headers):
  browser = await connect(browserWSEndpoint="ws://127.0.0.1:9222/devtools/browser/08e4e077-b178-4e23-951a-c8a016c571b5")
  page = await browser.newPage()
  cookies_for_pyppeteer = translate_burp_cookies_to_pyppeteer_cookies(cookies)
  await page.setCookie(*cookies_for_pyppeteer)
  await page.setExtraHTTPHeaders(headers)
  await page.goto(url)

asyncio.get_event_loop().run_until_complete(
    main(url=burp0_url, cookies=burp0_cookies, headers=burp0_headers))
