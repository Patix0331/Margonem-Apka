class Apka:

    def signIn(self):
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

        from requests import post
        from hashlib import sha1
        
        _username = input("Podaj login: ").encode('ascii')
        _password = input("Podaj hasło: ").encode('ascii')

        _ph = sha1(b"mleczko"+_password).hexdigest()

        response = post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
            'l': _username,
            'ph': _ph
        })

        if("logged" in str(response.content)):
            return response

        else:
            raise Exception

    def chars(self):
        """A function that returns a list of characters in a user's account. 
        It takes them from the response of signIn function"""
        
        from requests import post
        from re import findall

        data = post("http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3", cookies = response.cookies)
        characters = findall(r'id":"(.*?)","nick":"(.*?)".*?"db":"#(.*?)"', data.text)

        return characters

        
account = Apka()
response = account.signIn()

chars = account.chars()

#only for test
for i in chars:
    print(i)