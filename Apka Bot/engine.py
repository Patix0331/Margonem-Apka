import apka #needed for cookies from previous request (loging requests)
from requests import post   
import re
from hashlib import md5


class Engine:
    _characterToken = ""
    _characterEvent = ""
    level = None
    _server = ""
    _id = ""

    def Initialize(self, server, characterId, level):
        """
        Returning info of character
        """

        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(server, level, self._characterToken)

        cookies = apka.cookies
        cookies.set("mchar_id", characterId)

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
                print("MobileToken = ",_characterToken)

            else:
                print("Error: Postać jest zarejestrowana na innym świecie!")
                raise Exception

        if level == 4:
            timestamp = re.match('{\n  "ev": (.*?),', data.text)

            if timestamp:
                _characterEvent = timestamp[1]

        return data

    def RefreshEvent(self):
        """Simple function which refresh _characterEvent value"""

        headers = {
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
            "X-Unity-Version":"5.6.2p4"
        }

        cookies = apka.cookies
        cookies.set("mchar_id", self._id)

        data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&mobile_token={}".format(self._server, self._id, self._characterToken), headers=headers, cookies=cookies)

        timestamp = re.match('{\n  "ev": (.*?),', data.text)
        if timestamp:
            _characterEvent = timestamp[1]
            return True
        return False

if __name__ == "__main__":
    engine = Engine()
    print(engine.Initialize("aldous", apka.chars[0][0], 1).text)
    print(engine._characterToken)