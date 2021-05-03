import asyncio
from pyppeteer import connect
from pyppeteer.page import Page
from pyppeteer.network_manager import Request


# started from:
#   https://techoverflow.net/2019/08/10/pyppetteer-minimal-network-request-interception-example/
# adapted with (the request_interception callback needed some massaging...):
#   https://github.com/pyppeteer/pyppeteer/issues/198

async def async_request_interception(request: Request):
  """ await page.setRequestInterception(True) would block the flow, the interception is enabled individually """
  # enable interception
  request.__setattr__('_allowInterception', True)
  if request.url.startswith('http'):
    # print(f"\nreq.url: {request.url}")
    # print(f"  req.resourceType: {request.resourceType}")
    # print(f"  req.method: {request.method}")
    # print(f"  req.postData: {request.postData}")
    # print(f"  req.headers: {request.headers}")
    # print(f"  req.response: {request.response}")
    pass
  if request.url.startswith("https://techoverflow.net/"):
    print(f"continuing request to url: {request.url}")
    return await request.continue_()
  else:
    print(f"blocking request to url: {request.url}")
    return await request.abort()


def sync_request_interception(request: Request):
  return asyncio.create_task(async_request_interception(request))


async def main():
  browser = await connect(browserWSEndpoint="ws://127.0.0.1:9222/devtools/browser/a1065ec7-c46b-4297-af1a-7fd87d17d199")
  page = await browser.newPage()

  await page.setRequestInterception(True)

  # either one works...
  # page.on('request', lambda request: asyncio.create_task(async_request_interception(request)))
  page.on('request', sync_request_interception)

  await page.goto('https://techoverflow.net', {'waitUntil': 'networkidle2'})


asyncio.run(main())
