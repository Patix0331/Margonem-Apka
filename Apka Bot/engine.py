import apka #needed for cookies from previous request (loging requests)
from requests import post   
import re
from tkinter import messagebox
_characterToken = ""
_characterEvent = ""
level = 1
server = "aldous"
useToken = True

url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(server, level, _characterToken)

cookies = apka.response.cookies
cookies.set("mchar_id", apka.chars[0][0])

headers = {
    "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
    "X-Unity-Version":"5.6.2p4"
}

data = post(url, headers=headers, cookies = cookies)
#in need of customization
matchToken = re.match('{\n  "mobile_token": "(.*?)"', data.text)
if level == 1:
        if matchToken:
           _characterToken = matchToken[1] #has to be hashed
        else:
            messagebox.showinfo("minitix", "something's wrong. Ta postać jest zarejestrowana na innym świecie.")
#todo:
elif level == 4:
    messagebox.showinfo("Minitix", "level 4")
print(data.text)
print(_characterToken)