from bs4 import BeautifulSoup
import requests

'''Grab something with requests, and put it through Beautiful soup to see some search matches'''

resp = requests.get("https://finance.yahoo.com/quote/NFLX/options?p=NFLX")

html = resp.content
soup = BeautifulSoup(html, features="html.parser")

option_tags = soup.find_all("option")
print(option_tags)
