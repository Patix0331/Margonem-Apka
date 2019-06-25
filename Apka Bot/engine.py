import apka #needed for cookies from previous request (loging requests)
from requests import post   
import re
from hashlib import md5

_characterToken = ""
_characterEvent = ""
level = 1
_server = "aldous"
_useToken = True
_id = apka.chars[0][0]

url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(_server, level, _characterToken)

cookies = apka.response.cookies
cookies.set("mchar_id", _id)

headers = {
    "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
    "X-Unity-Version":"5.6.2p4"
}

data = post(url, headers=headers, cookies = cookies)

if level == 1:
    mobile_token = re.match('{\n  "mobile_token": "(.*?)"', data.text)
    if mobile_token:
        salt = "humantorch-".encode('utf-8')
        _characterToken = md5(salt+mobile_token[1].encode('utf-8')).hexdigest()
    else:
        print("Ta postać jest zarejestrowana na innym świecie!")
        raise Exception

if level == 4:
    timestamp = re.match('{\n  "ev": (.*?),', data.text) # CZEMU TO KURWA NIE DZIALA???
    if timestamp:
        _characterEvent = timestamp[1]

print("Token = ", _characterToken)
print("Event = ", _characterEvent)

data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&mobile_token={}".format(_server, _id, _characterToken), headers=headers, cookies=cookies)
timestamp = re.match('{\n  "ev": (.*?),', data.text)
if timestamp:
    _characterEvent = timestamp[1]
print("Event2 = ",_characterEvent)
