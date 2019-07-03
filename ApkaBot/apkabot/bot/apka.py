class Apka:
    
    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password

    def chars(self, cookies=None):
        from re import findall
        from requests import post
        
        data = post("http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3", cookies = cookies)
        characters = findall(r'id":"(.*?)","nick":"(.*?)".*?"poziom":"(.*?)".*?"prof":"(.*?)".*?"db":"#(.*?)".*?"stamina":(.*?)}', data.text)
        return characters, cookies

    def signIn(self):
        from requests import post
        from requests import post
        from hashlib import sha1
        
        login = self.login.encode('ascii')
        password = self.password.encode('ascii')

        ph = sha1(b"mleczko"+password).hexdigest()

        response = post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
            'l':login,
            'ph':ph
        })

        if("logged" in str(response.content)):
            return self.chars(response.cookies)
        else:
            raise Exception