import asyncio
from pyppeteer import connect, launch
from pyppeteer.page import Page
from pyppeteer.network_manager import Request, Response


# based off of : 2_intercept_pyppeteer_request.py

acceptable_url_prefixes = ["https://www.office.com/", "https://officehome.cdn.office.net", "https://officehome.cdn.office.net", "https://login.live.com", "https://content.lifecycle.office.net", "https://shell.cdn.office.net"]

async def async_request_interception(request: Request):
  """ await page.setRequestInterception(True) would block the flow, the interception is enabled individually """
  # enable interception
  request.__setattr__('_allowInterception', True)

  if not any(request.url.startswith(x) for x in acceptable_url_prefixes):
    # print(f"denying request to url: {request.url}")
    return await request.abort()

  # disable select javascript
  if request.resourceType == 'script': 
    if request.url.find("officebrowserfeedback") > 0:
      print(f"denying javascript request to url: {request.url}")
      return await request.abort()

  # default accept
  # print(f"accepting by default a request to: {request.url}")
  return await request.continue_()


async def async_allow_and_log(request: Request):
  print(f"allowing: req.url: {request.url}")
  # print(f"  req.resourceType: {request.resourceType}")
  # print(f"  req.method: {request.method}")
  # print(f"  req.postData: {request.postData}")
  # print(f"  req.headers: {request.headers}")
  # print(f"  req.response: {request.response}")
  # print(f"\n")
  return await request.continue_()


def sync_request_interception(request: Request):
  return asyncio.create_task(async_request_interception(request))


async def get_existing_browser_websocket_url() -> str:
  import aiohttp
  async with aiohttp.ClientSession() as session:

    try:
      async with session.get("http://localhost:9222/json/version") as response:
        chrome_details = await response.json()
        return chrome_details['webSocketDebuggerUrl']
    except aiohttp.ClientConnectorError:
      print("no running debuggable chromium found")


async def main():
  browserWSEndpoint = await get_existing_browser_websocket_url()

  browser = None
  if browserWSEndpoint:
    browser = await connect(browserWSEndpoint=browserWSEndpoint)
  else:
    browser = await launch(headless=False, executablePath="chromium", userDataDir="local_chrome_data")

  page = await browser.newPage()

  await page.setRequestInterception(True)

  page.on('request', sync_request_interception)

  await page.goto('https://www.office.com/?auth=1')
  await page.screenshot(path='example.png')
  await page.screenshot(path='full_example.png', fullPage=True)
  # await browser.close()


asyncio.run(main())
