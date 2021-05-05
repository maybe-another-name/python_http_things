# Overview

Some python scripts showing interactions with various HTTP-based libraries.

# Installation

    python3 -m venv venv
    source venv
    pip install requests
    pip install beautifulsoup4
    pip install requests-html
    pip install aiohttp
    pip install pyppeteer

# Burp Integration

The extension 'Copy As Python-Requests' is very handy (allowing copy & paste between burp & requests).

# Pyppeteer Integration

Several scripts; *__'2_intercept_pyppeteer_request.py'__* will look for a Chromium-based browser started with the relevant arguments; if none is found, then it will launch a new instance.

### Relevant Chromium Star Integration

There are a variety of flags available for Chromium on startup.  Example documentation for one of them can be found here: https://chromium.googlesource.com/chromium/src/+/master/docs/user_data_dir.md; and a full documentation can be found here: https://www.chromium.org/developers/how-tos/run-chromium-with-flags

Our example can be run with something like this:
>*__'chromium --remote-debugging-port=9222 --user-data-dir=local_chrome_data --proxy-server="http://127.0.0.1:8080"'__*
(This expects a proxy, like Burp, to be running at the relevant port.  That can be excluded if not desired.)