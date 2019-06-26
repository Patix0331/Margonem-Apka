import apka #needed for cookies from previous request (loging requests)
from requests import post   
import re
from hashlib import md5
import time

starttime = time.time()
class Engine:
    _characterToken = ""
    _characterEvent = ""
    level = None
    charnumber = int(input("Wprowadź numer postki do expienia:"))
    character = apka.chars1[charnumber] #todo: choose character menu #
    _server = character[4]
    _id = character[0]
    print("Wybrałeś postać: " + character[1] + " (" + character[2] + character[3] + ") [" + _server + "]")

    _cookies = apka.cookies1
    _headers = {
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
            "X-Unity-Version":"5.6.2p4"
        }

    def Initialize(self, level):
        """
        Returning info of character
        """
        useToken = True #???
        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(self._server, level, self._characterToken)

        cookies = Engine._cookies
        cookies.set("mchar_id", self._id)

        headers = Engine._headers

        data = post(url, headers=headers, cookies = cookies)

        if level == 1:
            mobile_token = re.match('{\n  "mobile_token": "(.*?)"', data.text)

            if mobile_token:
                salt = "humantorch-".encode('utf-8')
                self._characterToken = md5(salt+mobile_token[1].encode('utf-8')).hexdigest()

            else:
                print("Error: Postać jest zarejestrowana na innym świecie!")
                raise Exception

        if level == 4:
            timestamp = re.match('{\n  "ev": (.*?),', data.text)

            if timestamp:
                self._characterEvent = timestamp[1]

        return data

    def RefreshEvent(self):
        """Simple function which refresh _characterEvent value"""

        headers = Engine._headers

        cookies = Engine._cookies
        cookies.set("mchar_id", self._id)

        currentTime = time.time()
        data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=headers, cookies=cookies)

        #timestamp = re.match('{\n  "ev": (.*?),', data.text)  < ---------- ? 
        #if timestamp:
        #    self._characterEvent = timestamp[1]
        #   return True
        #return False
        return data
    def StartFight(self, town):
        self.town = town
        headers = Engine._headers
        cookies = Engine._cookies
        cookies.set("mchar_id", self._id)
        currentTime = time.time()
        #initiating fight:
        attackmanual = post("http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.town, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=cookies)
        time.sleep(0.1)
        currentTime = time.time()
        #fight in auto-mode
        turnAutoMode = post("http://{}.margonem.pl/engine?t=fight&a=f&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=cookies)
        return turnAutoMode
    def QuitFight(self):
        headers = Engine._headers
        cookies = Engine._cookies
        cookies.set("mchar_id", self._id)
        currentTime = time.time()
        #quit pending fight
        quitCurrentFight = post("http://{}.margonem.pl/engine?t=fight&a=quit&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=cookies)
        return quitCurrentFight


        
#initialize should be available from bot.py
if __name__ == "__main__":
    engine = Engine()
    for i in range(1, 5):
        data = engine.Initialize(i)
        #print("\n\nOdpowiedz kurwa z lvl 1: \n\n", data.text)
        #print(i)
afterlogin = engine.RefreshEvent()
    #print(afterlogin.text)
#just for tests. 
ilestaminy = 10
for i in range(1, ilestaminy):
    waitTime = 0.2
    fight = engine.StartFight("2675")
    time.sleep(waitTime)
    afterfight = engine.RefreshEvent()
    time.sleep(waitTime)
    quitfight = engine.QuitFight()
    afterfight = engine.RefreshEvent()
    time.sleep(waitTime)
stoptime = time.time()
worktime = round(stoptime - starttime, 2)
print("Zbicie " + str(ilestaminy) + " staminy zajęło " + str(worktime) + "s")