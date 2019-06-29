import apka #needed for cookies from previous request (loging requests)
from requests import post   
import re
from hashlib import md5
import time
re.DOTALL
starttime = time.time()
class Engine:
    _characterToken = ""
    _characterEvent = ""
    level = None
    _charnumbers = []
    _id = apka.userid
    _stamina = 50
    _server = ""
    _cookies = apka.cookies1
    _CharIterator = -1
    _HealItems = []
    _maxHP = 0
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
                    self._charnumbers.append(charnumber)
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
            if Engine._server == character[4]:
                time.sleep(5)
            else:
                Engine._server = character[4]
            print("character 0 to: " + character[0])

            Engine._cookies.set("mchar_id", character[0])

            print(character[1])
            self._stamina = 50
            for i in range(1,5):
                data = engine.Initialize(i)
    def Initialize(self, level):
        """
        Returning info of character
        """
        self.level = level
        useToken = True #???
        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(self._server, self.level, self._characterToken)

        data = post(url, headers=Engine._headers, cookies = Engine._cookies)
        #print("INITIALIZE" + str(self.level) + data.text)
        if level == 1:
            mobile_token = re.match('{\n  "mobile_token": "(.*?)"', data.text)

            if mobile_token:
                salt = "humantorch-" + mobile_token[1]
                salt = salt.encode('utf-8')
                self._characterToken = md5(salt).hexdigest()
            else:
                print("Error: Postać jest zarejestrowana na innym świecie!")
                raise Exception
            waitFor = re.search(r'"wait_for": "(.*?) ', data.text)
            print(waitFor)
            if waitFor:
                if waitFor[1] == "Poczekaj...":
                    print("waitfor5s")
                    time.sleep(10)
                    self.Initialize(1)
                    print(data.text)

                elif waitFor[1] == "Twoja":
                    print("waitfor30s")
                    time.sleep(30)
                    self.Initialize(1)
                    print("fucking podział łupów") #or pending fight (idk how)
                else:
                    print("waitfor, idk for what")
            maxhp = re.search('"maxhp": (\d*?),', data.text)
            print(maxhp[1])

        if level == 3:
            HealItems = []
            heals = re.findall(r'"id": (\d*?),.*?\s*"stat": ".*?;leczy=(\d*?);', data.text, re.DOTALL)
            
            for healitem in heals:
                if int(healitem[1]) > 0:
                    HealItems.append(healitem[0])
            print(HealItems)

        if level == 4:
            timestamp = re.match('{\n  "ev": (.*?),', data.text)

            if timestamp:
                self._characterEvent = timestamp[1]
        #print(data.text)
        time.sleep(1)
        return data
    def Heal():
        pass
        #post Heal
        '''regexhp = 

        regexmaxhp = 

        while hppercent < 75:
            
            if last stack: (amount = 0)
                delete from array'''




    def Sell(self, item):
        print("SELL")
        currentTime = time.time()
        self.item = item
        self.QuitFight()
        time.sleep(0.2)
        x = "http://{}.margonem.pl/engine?t=loot&not=&want={}&must=&final=1&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, self._id, currentTime, self._characterToken)
        print(x)
        accept = post("http://{}.margonem.pl/engine?t=loot&not=&want={}&must=&final=1&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies = Engine._cookies)
        time.sleep(0.2)
        currentTime = time.time()
        
        '''data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        time.sleep(0.2)
        sell = post("http://{}.margonem.pl/engine?t=shop&sell={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies = Engine._cookies)
        time.sleep(0.2)'''
        y = "http://{}.margonem.pl/engine?t=shop&sell={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, self._id, currentTime, self._characterToken)
        print(y)
        sell = post("http://{}.margonem.pl/engine?t=shop&sell={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies = Engine._cookies)
        print("\t\t\t\t\t\t sell text" + sell.text)
        print("sellnąłem coś")
        time.sleep(5)
        pass
    def RefreshEvent(self):
        print("REFRESH")
        """Simple function which refresh _characterEvent value"""
    
        currentTime = time.time()
        data = post("http://{}.margonem.pl/engine?t=_&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
  #      hpp = re.search('"hpp": (.*?),', data.text)
#        print("hp from ref")
 #       print(hpp)
        
        #hppercent = int(hpp[1])
        #print(hppercent)
        #if hppercent < 75:
            #self.Heal()
        time.sleep(0.5)
        loot = re.findall(r'"item":.*?"(.*?)".*?"hid"', data.text, re.DOTALL)
        print(loot)
        if len(loot) > 0:
            print(loot)
            for item in loot:
                self.QuitFight()
                time.sleep(0.2)
                self.Sell(item)
        else:
            self.QuitFight()
                #self.Sell(item[1])
        #timestamp = re.match('{\n  "ev": (.*?),', data.text)  < ---------- ? 
        #if timestamp:
        #    self._characterEvent = timestamp[1]
        #   return True
        #return False
        return loot
    def Fight(self, town):
        print("FIGHT")
        self.town = town
        currentTime = time.time()

        attackmanual = post("http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.town, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        #print(attackmanual.text)
        reload = re.match('{\n  "e": "Błąd wewnętrzny: Pominięty pakiet danych inicjujących"', attackmanual.text)
        if reload:
            print('znalazlem bleda')
        stamina = re.search(r'"stamina": (.*?),', attackmanual.text)
        if stamina:
            self._stamina = stamina[1]
            print("\n\nStamina left: ", self._stamina)
            if self._stamina == 0 or self._stamina == "0":
                    time.sleep(5)
                    self.AutoMode() 
                    self.QuitFight() #fight is still not closed after that, FIX NEEDED
                    time.sleep(5)
                    self.ChangeChar()
        
        
            #print("Start fight.", attackmanual.text)

    def AutoMode(self):
        print("AUTOMODE")

        currentTime = time.time()
        turnAutoMode = post("http://{}.margonem.pl/engine?t=fight&a=f&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        
        time.sleep(0.2)
    def QuitFight(self):
        print("QUITFIGHT")
        currentTime = time.time()
        #quit pending fight
        quitCurrentFight = post("http://{}.margonem.pl/engine?t=fight&a=quit&aid={}&mobile=1&ev={}&mobile_token={}".format(self._server, self._id, currentTime, self._characterToken), headers=Engine._headers, cookies=Engine._cookies)
        #print("\nZakończenie walki" + quitCurrentFight.text)
    def FightAndRelog(self):
        pass

                    





engine = Engine()
chooseChars = engine.ChooseCharacters()
while True:
        awaitime = 1
        while engine._stamina != 0:
            engine.Fight("2675")
            time.sleep(awaitime)
            engine.AutoMode()
            #http://aldous.margonem.pl/engine?t=loot&not=&want=572986876&must=&final=1&aid=9045851&mobile=1&ev=1561816451.748353&mobile_token=52d6675a2a926b2e839905b1f5813a05
            # + sell
            time.sleep(awaitime)
            engine.RefreshEvent() 

        engine.ChangeChar()

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