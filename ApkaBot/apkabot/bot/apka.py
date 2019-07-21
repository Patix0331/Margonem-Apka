from requests import post
import asyncio
from json import loads
from time import time, sleep

class Account():

    def __init__(self, login, password, proxy=None):
        self.login = login
        self.password = password
        self.proxy = proxy
        self.headers = {
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; Samsung Galaxy S8 - 8.0 - API 26 - 1440x2960 Build/OPR6.170623.017)",
            "X-Unity-Version":"5.6.2p4"
            #'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0.0; HUAWEI VNS-L21 Build/HUAWEIVNS-L21)',
            #'X-Unity-Version':'5.6.7f1'
        }
        self.maps = dict()
        self.items = dict()

    def signIn(self):

        from hashlib import sha1

        url = 'https://www.margonem.pl/ajax/logon.php?t=login'

        password = self.password.encode('utf8')
        hashed_password = sha1(b"mleczko"+password).hexdigest()

        data = {'l':self.login,'ph':hashed_password}

        response = post(url, data = data, proxies=self.proxy)

        self.cookies = response.cookies

        if not response.cookies:
            exit()

    def get_chars(self):
        
        url = 'http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3'

        response = post(url, cookies = self.cookies, proxies = self.proxy)
        data = loads(response.text)
        characters = dict()

        for i in data['charlist']:

            item = data['charlist'][i]

            characters[i] = {
                'nick':item['nick'],
                'lvl':int(item['lvl']),
                'profesja':item['prof'],
                'clan':None,
                'world':item['db'][1:],
                'max_hp':int(item['max_zycie']),
                'atm_hp':int(item['zycie']),
                'free_space':5,
                'stamina':int(item['stamina']),
                'token':None,
                'stamina_pots':dict(),
                'pots':dict(),
                'settings':{
                    'sell':True,
                    'heal_from':70,
                    'use_stamina':True,
                    'use_fullheal':True,
                    'send_gold':False,
                    'use_bless':None
                }
            }

            try:
                characters[i]['clan'] = item['clanname']
            except KeyError:
                pass

        self.characters = characters

    def Initialize(self, level, char):

        self.cookies['mchar_id'] = char
        url = "http://{}.margonem.pl/engine?t=init&initlvl={}&mobile=1&mobile_token={}".format(
            self.characters[char]['world'], level, self.characters[char]['token'])

        response = post(url, headers=self.headers, cookies = self.cookies, proxies=self.proxy)
        data = loads(response.text)

        if level == 1:

            from hashlib import md5

            token = ("humantorch-" + data['mobile_token']).encode('utf-8')
            self.characters[char]['token'] = md5(token).hexdigest()

        elif level == 2:

            if len(self.maps) == 0:
                for map in data['mobile_maps']:
                    self.maps[map] = data['mobile_maps'][map]['name']

        elif level == 3:

            for i in data['item']:

                if 'leczy' in data['item'][i]['stat']:

                    stats = data['item'][i]['stat'].split(';')

                    if int(stats[3].split('=')[1]) < 50:
                        continue

                    self.characters[char]['pots'][data['item'][i]['id']] = {
                        'amount' : int(stats[0].split('=')[1]),
                        'heal' : int(stats[3].split('=')[1])
                    }

                elif 'fullheal' in data['item'][i]['stat']:

                    stats = data['item'][i]['stat'].split(';')

                    self.characters[char]['pots'][data['item'][i]['id']] = {
                        'amount' : 'fullheal',
                        'heal' : int(stats[0].split('=')[1])
                    }
                
                elif 'stamin' in data['item'][i]['stat']:

                    stats = data['item'][i]['stat'].split(';')

                    self.characters[char]['stamina_pots'][data['item'][i]['id']] = {
                        'amount' : int(stats[0].split('=')[1]),
                        'add' : int(stats[6].split('=')[1])
                    }

    def refresh(self, char):

        sleep(0.5)
        url = 'http://{}.margonem.pl/engine?t=_&mobile=1&ev={}&mobile_token={}'.format(self.characters[char]['world'], time(), self.characters[char]['token'])

        response = post(url, headers = self.headers, cookies = self.cookies, proxies = self.proxy)

        data = loads(response.text)

        #checking is logged
        try:
            if "Nie jesteś zalogowany" in data['alert']:
                exit()
        except:
            pass

        #checking is loot
        try:
            if data['item']:
                self.items = data['item']

        except KeyError:
            pass

        #checking hp
        try:
            self.characters[char]['max_hp'] = int(data['h']['maxhp'])
            self.characters[char]['atm_hp'] = int(data['h']['hp'])

        except KeyError:
            pass

        #get stamina
        try:
            self.characters[char]['stamina'] = int(data['h']['stamina'])
        except KeyError:
            pass

    def start_fight(self, town, char):

        from sys import exit

        sleep(1)
        url = "http://{}.margonem.pl/engine?t=fight&a=attack&town_id={}&mobile=1&ev={}&mobile_token={}".format(
            self.characters[char]['world'], town, time(), self.characters[char]['token'])

        response = post(url, headers = self.headers, cookies = self.cookies, proxies=self.proxy)

        data = loads(response.text)
        print(data)

    def auto_fight(self, char):

        sleep(1)       
        url = "http://{}.margonem.pl/engine?t=fight&a=f&mobile=1&ev={}&mobile_token={}".format(
            self.characters[char]['world'], time(), self.characters[char]['token'])

        post(url, headers = self.headers, cookies = self.cookies, proxies=self.proxy)

    def quit_fight(self, char):

        sleep(1)
        url = "http://{}.margonem.pl/engine?t=fight&a=quit&mobile=1&ev={}&mobile_token={}".format(
            self.characters[char]['world'], time(), self.characters[char]['token'])


        post(url, headers = self.headers, cookies = self.cookies, proxies=self.proxy)

            

    def selling_items(self, items, char):

        #accept loot
        _items = ""
        for i in items:
            _items += i+","

        url = 'http://{}.margonem.pl/engine?t=loot&not=&want={}&must=&final=1&mobile=1&ev={}&mobile_token={}'.format(
            self.characters[char]['world'], _items[:-1], time(), self.characters[char]['token'])

        sleep(0.5)
        response = post(url, headers = self.headers, cookies = self.cookies, proxies = self.proxy)

        data = loads(response.text)
        try:
            self.characters[char]['free_space'] = int(data['loot']['free'])
        except KeyError:
            pass
        
        #selling items
        _items = ""

        for i in items:

            if self.characters[char]['free_space'] <= 5:
                _items += i+","

            else:

                not_sell = ['legenda', 'heroik', 'unikat']

                for j in not_sell:

                    if j in items[i]['stat']:
                        continue

                else:
                    _items += i+","
        
        url = 'http://{}.margonem.pl/engine?t=shop&sell={}&mobile=1&ev={}&mobile_token={}'.format(
            self.characters[char]['world'], _items[:-1], time(), self.characters[char]['token'])

        sleep(0.5)
        response = post(url, headers = self.headers, cookies = self.cookies, proxies = self.proxy)
        self.items.clear()

    def healing(self, char):

        while 100 * ( self.characters[char]['atm_hp'] / self.characters[char]['max_hp'] ) < self.characters[char]['settings']['heal_from']:

            for potion in self.characters[char]['pots']:

                #skip fullheal potions if disabled by user
                if not self.characters[char]['settings']['use_fullheal']:
                    if 'fullheal' in self.characters[char]['pots'][potion]['amount']:
                        continue
                    

                url = 'http://{}.margonem.pl/engine?t=moveitem&id={}&st=1&mobile=1&ev={}&mobile_token={}'.format(
                    self.characters[char]['world'], potion, time(), self.characters[char]['token'])

                response = post(url, headers=self.headers, cookies = self.cookies, proxies = self.proxy)
                data = loads(response.text)

                try:
                    if data['item'][potion]['del']:
                        self.characters[char]['pots'].pop(potion, None)
                except KeyError:
                    pass

                self.characters[char]['atm_hp'] = data['h']['warrior_stats']['hp']

                try:
                    self.characters[char]['pots'][potion]['amount'] -= 1
                except TypeError:
                    pass
                
                break

    #TODO
    def use_stamina(self, char):
        # if self.characters[char]['stamina'] <= 2:
        #     for potion in self.characters[chars]['stamina_pots']:
        #         url = stamina XD
        pass

    async def run(self, chars, time):

        from datetime import datetime

        self.signIn()

        self.get_chars()
              
        while datetime.now() < time:
            sleep(0.5)
            for char in chars:
                sleep(0.5)
                #if license is not valid then exit()
                if datetime.now() > time or not time:
                    exit()

                for init in range(1,5):

                    self.Initialize(init, char)

                while self.characters[char]['stamina'] > 0:
                    sleep(0.1)

                    self.start_fight(chars[char]['map'], char)

                    self.auto_fight(char)

                    self.refresh(char)

                    self.quit_fight(char)

                    if self.characters[char]['settings']['sell'] or self.characters[char]['free_space'] <= 5:
                        if self.items:
                            self.selling_items(self.items, char)

                    self.healing(char)

                    self.use_stamina(char)


if __name__ == "__main__":
    acc = Account('login','password')
    acc.run(chars={'id_postaci':{'map':'id_mapy'}}, time="license left")