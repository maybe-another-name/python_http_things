import asyncio
from pyppeteer import connect
from pyppeteer.page import Page
from pyppeteer.network_manager import Request, Response


# started from:
#   https://techoverflow.net/2019/08/10/pyppetteer-minimal-network-request-interception-example/
# adapted with (the request_interception callback needed some massaging...):
#   https://github.com/pyppeteer/pyppeteer/issues/198

async def async_request_interception(request: Request):
  """ await page.setRequestInterception(True) would block the flow, the interception is enabled individually """
  # enable interception
  request.__setattr__('_allowInterception', True)

  if not request.url.startswith("https://techoverflow.net/"):
    print(f"denying request to url: {request.url}")
    return await request.abort()

  if request.resourceType == 'script':
    print(f"allowing the download of a script from: {request.url}")
    return await async_allow_and_log(request)
  if request.resourceType == 'image':
    print(f"denying the download of an image from: {request.url}")
    return await request.abort()
  if request.resourceType == 'other':
    print(f"denying the download of something from: {request.url}")
    return await request.abort()

  if request.method == 'GET':
    print(f"allowing a GET method to: {request.url}")
    return await async_allow_and_log(request)

  if request.method == 'POST':
    print(f"denying a POST method to: {request.url}")
    return await request.abort()

  # default deny
  print(f"denying by default a request to: {request.url}")
  return await request.abort()


async def async_allow_and_log(request: Request):
  # print(f"req.url: {request.url}")
  # print(f"  req.resourceType: {request.resourceType}")
  # print(f"  req.method: {request.method}")
  # print(f"  req.postData: {request.postData}")
  # print(f"  req.headers: {request.headers}")
  # print(f"  req.response: {request.response}")
  # print(f"\n")
  return await request.continue_()


def sync_request_interception(request: Request):
  return asyncio.create_task(async_request_interception(request))

def sync_response_inspection(response: Response):
  # print(f"response.url: {response.url}")
  # print(f"  req.status: {response.status}")
  # print(f"  req.request.method: {response.request.method}")
  # print(f"  req.request.postData: {response.request.postData}")
  # print(f"  req.headers: {response.headers}")
  # print(f"\n")


async def main():
  browser = await connect(browserWSEndpoint="ws://127.0.0.1:9222/devtools/browser/026206f8-2769-4072-b0b1-00b24d7bdadc")
  page = await browser.newPage()

  await page.setRequestInterception(True)

  # either one works...
  # page.on('request', lambda request: asyncio.create_task(async_request_interception(request)))
  page.on('request', sync_request_interception)
  page.on('response', sync_response_inspection)

  await page.goto('https://techoverflow.net')
  await page.screenshot(path='example.png')
  await page.screenshot(path='full_example.png', fullPage=True)
  await browser.close()


asyncio.run(main())
