    #_login = "x"
    #_password = "y"

from requests import *
from hashlib import *
from re import findall

def signIn(login, password):
        """Return response of log in post request
        Take default values from user input.
        
        Raises
        ------
        Exception
            Error with request login

        Returns
        -------
        response
            response of login post request
        """
        login = login.encode('ascii')
        password = password.encode('ascii')
        

        _ph = sha1(b"mleczko"+password).hexdigest()

        response = post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
            'l': login,
            'ph': _ph
        })

        if("logged" in str(response.content)):
            return response.cookies

        else:
            print("BŁĘDNE DANE LOGOWANIA")

            raise Exception

def chars(cookies):
        """A function that returns a list of characters in a user's account. 
        It takes them from the response of signIn function"""

        data = post("http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3", cookies = cookies)
        characters = findall(r'id":"(\d*?)","nick":"(.*?)".*?"poziom":"(\d*?)".*?"prof":"(\w)".*?"db":"#(\w*)".*?"stamina":(.*?)}', data.text)
        return characters
#signIn = apka.signIn()
#in case of multiple accounts object renamed cookies - > cookies1 and chars - > chars1
#login = apka.signIn("app", "1234")
#userid = signIn["user_id"]
#chars1 = apka.chars(signIn)
#only folr test
""""#chars: 0 - id, 1 - nick, 2 - lvl, 3 - prof, 4 - world, 5 - stamina
c = 0
for i in chars1:
    print(i[1] + " (" + i[2] + i[3] + ") [" + i[4] + "] - " + i[0] +" pozostało " + i[5] + " staminy " + "NUMER POSTACI:" + str(c))
    c += 1""" 