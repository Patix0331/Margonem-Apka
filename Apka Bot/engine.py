import apka #needed for cookies from previous request (loging requests)
from requests import post   
from re import findall

_characterToken = ""
_characterEvent = ""
level = 1
server = "aldous"
useToken = True

url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1{}&mobile_token={}".format(server, level, useToken, _characterToken)

cookies = apka.response.cookies
cookies.set("mchar_id", apka.chars[0][0])

headers = {
    "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
    "X-Unity-Version":"5.6.2p4"
}

data = post(url, headers=headers, cookies = cookies)
print(data.text)