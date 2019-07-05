from requests import post   
import re
from hashlib import md5
import time
import json

class Engine():
    _characterToken = None
    _characterEvent = None
    level = None
    logged = True
    _charnumbers = None
    _stamina = 50
    _server = ""
    _CharIterator = -1
    _HealItems = None
    _maxHP = 0
    _previousMap = None
    _unlockMap = False
    _map = None
    _headers = {
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
            "X-Unity-Version":"5.6.2p4"
        }
    def __init__(self, cockie, characters, chosen):
        self._cookies = cockie
        print("Init cookies: ", self._cookies)
        self._characters = characters
        print("Init characters: ", self._characters)
        self._charnumbers = chosen
        self.ChangeChar()
    


    '''def ChooseCharacters(self):
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
        self.ChangeChar()'''
    def ChangeChar(self):
            if self._CharIterator + 1 != len(self._charnumbers):
                self._CharIterator += 1
            else:
                self._CharIterator = 0

            character = self._characters[self._charnumbers[self._CharIterator]]
            if self._server == character[4]:
                time.sleep(10)
            else:
                self._server = character[4]
            print("Teraz expi: " + character[0])

            self._cookies["mchar_id"] = character[0]
            print("Character[1] - chuj wie co to: ", character[1])
            self._stamina = 50
            for i in range(1,5):
                time.sleep(0.5)
                data = self.Initialize(i)

    def Initialize(self, level):
        """
        Returning info of character
        """
        self.level = level
        useToken = True #???
        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(self._server, self.level, self._characterToken)
        print('Init nr ', self.level)
        data = post(url, headers=self._headers, cookies = self._cookies)
        #print("INITIALIZE" + str(self.level) + data.text)
        if level == 1:
            mobile_token = re.match('{\n  "mobile_token": "(.*?)"', data.text)

            if mobile_token:
                salt = "humantorch-" + mobile_token[1]
                salt = salt.encode('utf-8')
                self._characterToken = md5(salt).hexdigest()
            else:
                print("Error: Postać jest zarejestrowana na innym świecie! ALBO PRZERWA TECHNIAWKA")
                time.sleep(600)
                self.ChangeChar()
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
            lvl = re.search(r'"lvl": (\d*?),', data.text)
            
            if lvl:
                print("Level: ", lvl[1], "postaci: ", self)
                levelek = int(lvl[1])
                mapky = ['2675', '2676', '2677', '2794', '2795', '2796', '2797', '2798', '2799', '2800', '2801', '2802', '2803', '2804', '2805', '2806', '2807', '2808', '2809', '2810', '2829', '2830', '2831', '2832', '2833', '2834', '2835', '2836', '2837', '2838', '2839', '2840', '2841', '2842', '2843', '2844', '2845', '2846', '2847', '2848', '2849', '2850', '2851', '2852', '2853', '2854', '2855', '2856', '2857', '2858', '2859', '3977', '3978', '3979', '3980', '3981', '3982', '3983', '3984', '3985']
                #mapkyelite = ['100318', '100319', '101250', '101251', '101252', '101253', '101254', '101255', '101256', '101257', '104715', '104716', '104717', '104718', '104719', '104720', '104721', '104722', '104723', '104724']
                place = round(levelek // 5.1) - 1
                self._map = mapky[place]
                if place > 0:
                    self._previousMap = mapky[place - 1]
                else: 
                    self._previousMap = ""

                print(self._map)
            else: 
                self.Initialize(1)
        if level == 2:
            if self._previousMap != "":
                myregex = self._previousMap
                print(myregex)
                isMapLocked = re.search(myregex + r'": \n    {\n      "name": "(.*?)",\n      "bg": "(.*?)",\n      "done": (.?),', data.text)
                print(isMapLocked)
                print(isMapLocked[1])
                print(isMapLocked[2])
                print(isMapLocked[3])
                if isMapLocked[3] == "0":
                    self._unlockMap = True

        if level == 3:
            self._HealItems = []
            heals = re.findall(r'"id": (\d*?),\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?"stat": ".*?;leczy=(\d*?);', data.text)
            print(heals)
            for healitem in heals:
                if int(healitem[1]) > 0:
                    self._HealItems.append(healitem[0])
            print(self._HealItems)

        if level == 4:
            timestamp = re.match('{\n  "ev": (.*?),', data.text)

            if timestamp:
                self._characterEvent = timestamp[1]
        #print(data.text)
        time.sleep(1)
        return data
    def Heal(self):
        print("HEAL")
        hppercent = 0
        time.sleep(0.5)
        while hppercent < 75 and len(self._HealItems) > 0:
            print("INFINITY LOOP")
            time.sleep(0.5)
            currentTime = time.time()
            x = "http://{}.margonem.pl/engine?t=moveitem&id={}&st=1&mobile=1&ev={}&mobile_token={}".format(self._server, self._HealItems[0], currentTime, self._characterToken)
            print(x)
            healme = post("http://{}.margonem.pl/engine?t=moveitem&id={}&st=1&mobile=1&ev={}&mobile_token={}".format(self._server, self._HealItems[0], currentTime, self._characterToken), headers=self._headers, cookies = self._cookies)
            #neededref = re.search('"e": "ok"', healme.text)

            #if neededref:
            #   healme = post("http://{}.margonem.pl/engine?t=_&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
            print(healme.text)

            ifLastStack = re.search('"del": "1"', healme.text)
            print(ifLastStack)

            if ifLastStack:
                self._HealItems.pop(0)
            regexhp = re.search('"hp": (\d*?),', healme.text)
            regexmaxhp =  re.search('"maxhp": (\d*?),', healme.text)
            print("\t\t\t\t\t\t\t\t\thp")
            print(regexhp)
            if regexhp and regexmaxhp:
                print("if regexhp and regexmaxhp:")
                hp = int(regexhp[1])
                print(regexhp)
                regexmaxhp =  re.search('"maxhp": (\d*?),', healme.text)
                maxhp = int(regexmaxhp[1])
                hppercent = 100 * hp/maxhp
            else:
                hppercent = 0
            print(hppercent)





    def Sell(self, item):
        print("SELL")
        currentTime = time.time()
        self.item = item
        time.sleep(0.5)
        x = "http://{}.margonem.pl/engine?t=loot&not=&want={}&must=&final=1&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, currentTime, self._characterToken)
        print(x)
        accept = post("http://{}.margonem.pl/engine?t=loot&not=&want={}&must=&final=1&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, currentTime, self._characterToken), headers=self._headers, cookies = self._cookies)
        time.sleep(0.5)
        currentTime = time.time()
        
        sell = post("http://{}.margonem.pl/engine?t=shop&sell={}&mobile=1&ev={}&mobile_token={}".format(self._server, self.item, currentTime, self._characterToken), headers=self._headers, cookies = self._cookies)
        print("\t\t\t\t\t\t sell text" + sell.text)
        print("sellnąłem coś")
    def RefreshEvent(self):
        print("REFRESH")
        """Simple function which refresh _characterEvent value"""
        time.sleep(0.5)
        currentTime = time.time()
        data = post("http://{}.margonem.pl/engine?t=_&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
        print(data.text)
        refresh = re.search('"t": "reload",', data.text)
        if refresh:
            for i in range(1,5):
                data = self.Initialize(i)

        hp = re.search('"hp": (\d*?),', data.text)
        maxhp = re.search('"maxhp": (\d*?),', data.text)
        hpp = None
        if hp and maxhp:
            hpp = 100 * int(hp[1])/int(maxhp[1])

        dead = re.search('"dead": (\d.?),', data.text)
        loot = re.findall(r'"item":.*?"(\d*?)".*?"hid"', data.text, re.DOTALL)
        time.sleep(0.5)
        self.QuitFight()
        time.sleep(0.5)
        if dead:
            time.sleep(int(dead[1]) + 2)
            self.Heal()
            currentTime = time.time()
            ref = post("http://{}.margonem.pl/engine?t=_&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)

        if hpp:
            print("hp from ref")
            print(hpp)
            if hpp < 75:
                self.Heal()
            currentTime = time.time()
            ref = post("http://{}.margonem.pl/engine?t=_&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)

        if len(loot) > 0:
            print(loot)
            for item in loot:
                self.Sell(item)
                #self.Sell(item[1])
        #timestamp = re.match('{\n  "ev": (.*?),', data.text)  < ---------- ? 
        #if timestamp:
        #    self._characterEvent = timestamp[1]
        #   return True
        #return False
        return loot
    def Fight(self):
        print("FIGHT")
        town = self._map
        print("\t\t\t\t\t\t\t\t" + town)
        currentTime = time.time()
        if self._unlockMap == True:
            town = self._previousMap
            print("ODBLOKOWUJĘ MAPĘ")
            c = "http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&boss_fight=1&mobile=1&ev={}&mobile_token={}".format(self._server, town, currentTime, self._characterToken)
            print
            attackmanual = post("http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&boss_fight=1&&mobile=1&ev={}&mobile_token={}".format(self._server, town, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
            self._unlockMap = False 
            print(attackmanual.text)
        else:
            print("ATAKUJE NORMALNIE")
            attackmanual = post("http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&mobile=1&ev={}&mobile_token={}".format(self._server, town, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
            
            a = json.loads(attackmanual.text)
            try:
                if "Nie jesteś zalogowany" in a['w']:
                    #print("Logout. Closing the bot")
                    self.logged = False
                
            except:
                try:
                    if "Nie jesteś zalogowany" in a['alert']:
                        #print("Logout. Closing the bot")
                        self.logged = False
                except:
                    pass
        
        #print(attackmanual.text)
        reload = re.match('{\n  "e": "Błąd wewnętrzny: Pominięty pakiet danych inicjujących"', attackmanual.text)
        if reload:
            print('znalazlem bleda')
        stamina = re.search(r'"stamina": (.*?),', attackmanual.text)
        if stamina:
            self._stamina = stamina[1]
            print("\n\nStamina left: ", self._stamina)
            if self._stamina == 0 or self._stamina == "0":
                    self.AutoMode() 
                    self.QuitFight() #fight is still not closed after that, FIX NEEDED
                    time.sleep(5)
                    self.ChangeChar()
        
        
            #print("Start fight.", attackmanual.text)

    def AutoMode(self):
        print("AUTOMODE")

        currentTime = time.time()
        turnAutoMode = post("http://{}.margonem.pl/engine?t=fight&a=f&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
    def QuitFight(self):
        print("QUITFIGHT")
        currentTime = time.time()
        #quit pending fight
        quitCurrentFight = post("http://{}.margonem.pl/engine?t=fight&a=quit&mobile=1&ev={}&mobile_token={}".format(self._server, currentTime, self._characterToken), headers=self._headers, cookies=self._cookies)
        #print("\nZakończenie walki" + quitCurrentFight.text)
        
            #print("Start fight.", attackmanual.text)
    def Run(self):
        while self.logged:
                while self._stamina != 0:
                    if self.logged is False:
                        break
                    self.Fight()
                    time.sleep(0.5)
                    self.AutoMode()
                    #http://aldous.margonem.pl/engine?t=loot&not=&want=572986876&must=&final=1&aid=9045851&mobile=1&ev=1561816451.748353&mobile_token=52d6675a2a926b2e839905b1f5813a05
                    # + sell
                    time.sleep(0.5)
                    a = self.RefreshEvent() 
                    time.sleep(0.5)

                self.ChangeChar()
#engine = Engine(apka.SignIn("app", "1234"))


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