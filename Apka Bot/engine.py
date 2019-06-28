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
    _charnumbers = []
    _id = 0
    _stamina = 50
    _server = ""
    _cookies = apka.cookies1
    _CharIterator = -1
    _headers = {
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
            "X-Unity-Version":"5.6.2p4"
        }

    def ChooseCharacters(self):
        while True:
            charnumber = input("By wystartować bota kliknij ENTER! Wprowadź numer postaci do expienia:  ")
            if charnumber == "" :
                break
            else:
                try:
                    charnumber = int(charnumber)
                    Engine._charnumbers.append(charnumber)
                except Exception:
                    print("By wystartować bota kliknij ENTER")
                    continue
        self.ChangeChar()
    def ChangeChar(self):
            if Engine._CharIterator + 1 != len(Engine._charnumbers):
                Engine._CharIterator += 1
            else:
                Engine._CharIterator = 0

            character = apka.chars1[Engine._charnumbers[Engine._CharIterator]]
            Engine._server = character[4]
            Engine._id = character[0]

            Engine._cookies.set("mchar_id", self._id)

            print(character[1])
            self._stamina = 50
            for i in range(1,5):
                data = engine.Initialize(i)
            self.Fight("2675")

    def Initialize(self, level):
        """
        Returning info of character
        """
        self.level = level
        useToken = True #???
        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(self._server, self.level, self._characterToken)

        data = post(url, headers=Engine._headers, cookies = Engine._cookies)
        print(data.text)
        if level == 1:
            mobile_token = re.match('{\n  "mobile_token": "(.*?)"', data.text)

            if mobile_token:
                salt = "humantorch-".encode('utf-8')
                self._characterToken = md5(salt+mobile_token[1].encode('utf-8')).hexdigest()

            else:
                print("Error: Postać jest zarejestrowana na innym świecie!")
                raise Exception
            waitFor = re.search(r'"wait_for": "(.*?) ', data.text)
            if waitFor:
                if waitFor[1] == "Poczekaj...":
                    print("waitfor5s")
                    time.sleep(10)
                    data = post(url, headers=Engine._headers, cookies = Engine._cookies)
                    print(data.text)

                elif waitFor[1] == "Twoja":
                    print("waitfor30s")
                    time.sleep(30)
                    data = post(url, headers=Engine._headers, cookies = Engine._cookies)
                    print("fucking podział łupów") #or pending fight (idk how)
                else:
                    print("waitfor, idk for what")
        if level == 4:
            timestamp = re.match('{\n  "ev": (.*?),', data.text)

            if timestamp:
                self._characterEvent = timestamp[1]
        print(data.text)
        time.sleep(1)
        return data

    def RefreshEvent(self):
        """Simple function which refresh _characterEvent value"""

        currentTime = time.time()
        data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)

        #timestamp = re.match('{\n  "ev": (.*?),', data.text)  < ---------- ? 
        #if timestamp:
        #    self._characterEvent = timestamp[1]
        #   return True
        #return False
        return data
    def Fight(self, town):

        self.town = town
        currentTime = time.time()

        attackmanual = post("http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.town, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        print(attackmanual.text)
        reload = re.match('{\n  "e": "Błąd wewnętrzny: Pominięty pakiet danych inicjujących"', attackmanual.text)
        if reload:
            print('znalazlem bleda')
        stamina = re.search(r'"stamina": (.*?),', attackmanual.text)
        if stamina:
            self._stamina = stamina[1]
            print("\n\nStamina left: ", self._stamina)
            if self._stamina == 0 or self._stamina == "0":
                    time.sleep(0.2)
                    self.AutoMode() #fight is still not closed after that, FIX NEEDED
                    time.sleep(0.2)
                    self.ChangeChar()
        
            
            #print("Start fight.", attackmanual.text)
        time.sleep(0.2)
        self.AutoMode()
        
    def AutoMode(self):

        currentTime = time.time()
        turnAutoMode = post("http://{}.margonem.pl/engine?t=fight&a=f&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        
        time.sleep(0.2)
        self.QuitFight()

    def QuitFight(self):
        currentTime = time.time()
        #quit pending fight
        quitCurrentFight = post("http://{}.margonem.pl/engine?t=fight&a=quit&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        #print("\nZakończenie walki" + quitCurrentFight.text)

        time.sleep(0.2)
        if self._stamina != 0 and self._stamina != "0":
            self.Fight("2675")
    def FightAndRelog(self):
        pass

                    


engine = Engine()
chooseChars = engine.ChooseCharacters()
#initialize should be available from bot.py
'''if __name__ == "__main__":
    for i in range(1, 5):
        data = engine.Initialize(i)
        #print("\n\nOdpowiedz kurwa z lvl 1: \n\n", data.text)
        #print(i)
afterlogin = engine.RefreshEvent()
    #print(afterlogin.text)
#just for tests. 
for i in range(1, 3):
    engine.Fight("2675")'''

stoptime = time.time()
worktime = round(stoptime - starttime, 2)
print("Zbicie staminy zajęło " + str(worktime) + "s")