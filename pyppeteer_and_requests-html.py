import asyncio

import pyppeteer
from pyppeteer.browser import Browser

from requests_html import HTMLSession


async def get_browser() -> Browser:
  '''
  this expects the browser with remote debugging enabled, for example:
    /.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome --remote-debugging-port=9222
  on most platforms this will then report it's id, as follows:
    DevTools listening on ws://127.0.0.1:9222/devtools/browser/e3b807df-40cb-4922-97bb-2e8ffc519d73
  (on windows this won't be reported, but can be queried through http://127.0.0.1:9222/json/)
  '''
  browser = await pyppeteer.connect(
      browserWSEndpoint="ws://127.0.0.1:9222/devtools/browser/f3c3ff05-276e-4b85-b510-b4b3029ab7c5")
  return browser

candidate_url = 'https://finance.yahoo.com/quote/NFLX/options?p=NFLX'


def main():

  session = HTMLSession()

  # wait for the browser to connect
  loop = asyncio.get_event_loop()
  browser = loop.run_until_complete(get_browser())

  session._browser = browser
  session.loop = loop

  response = session.get(candidate_url)

  response_html = response.html
  response_html.url = candidate_url

  response_html.render()

  print(response.html.html)

  # print(response.html)


main()
