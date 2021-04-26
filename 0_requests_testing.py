import requests
'''Uses the requests library with a custom header, and dumping the netflix stock prices to console...'''


def testing_get():
  print("testing get")
  headers = \
      {
          'Accept': 'application/vnd.github.v3.test-match+json',
          'set-cookie': 'cloud.session.token= blah; Max-Age=2592000; Expires=Wed, 28-Apr-2021 13:24:34 GMT; Domain=blah; Path=/; Secure; HttpOnly; SameSite=None'
      }

  response = requests.get(
      'https://finance.yahoo.com/quote/NFLX/options?p=NFLX', headers=headers)
  print(response)

  print("\n" + response.text)


testing_get()
