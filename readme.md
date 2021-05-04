Overview
===============

Some python scripts showing interactions with various HTTP-based libraries.

Installation
===============

    python3 -m venv venv
    source venv
    pip install requests
    pip install beautifulsoup4
    pip install requests-html
    pip install aiohttp
    pip install pyppeteer

Burp Integration
===============

The extension 'Copy As Python-Requests' is very handy (allowing copy & paste between burp & requests).

Pyppeteer Integration
===============

Several scripts; *__'2_intercept_pyppeteer_request.py'__* will look for a Chromium-based browser started with the relevant arguments; if none is found, then it will launch a new instance.