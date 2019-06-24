class Apka:
    
    from hashlib import sha1

    username = input("Podaj login: ").encode('ascii')
    password = input("Podaj hasło: ").encode('ascii')

    hashed_password = sha1(b"mleczko"+password).hexdigest()

    def signIn(self, username = username, ph=hashed_password):
        """Return response of log in post request
        Take default values from user input.

        Parameters
        ----------
        username : bytes
            Username entered by the user
        ph : bytes
            hashed 'mleczko'+password entered by the user with sha1 method
        
        Raises
        ------
        Exception
            Error with request login

        Returns
        -------
        response
            response of login post request
        """
        
        import requests
        response = requests.post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
            'l': username,
            'ph': ph
        })

        if("logged" in str(response.content)):
            return response

        else:
            raise Exception

    def chars(self):
        """A function that returns a list of characters in a user's account. 
        It takes them from the response of signIn function"""
        
        import json
        import requests

        id, server, nick = [], [], []

        data = requests.post("http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3", cookies = response.cookies)
        accounts = json.loads(data.text)

        for char in accounts['charlist']:

            info = accounts['charlist'][char]
            world = (info['db'])[1:]

            id.append(info['id'])
            server.append(world)
            nick.append(info['nick'])
            
        characters = list(zip(id,server,nick))
        return characters

        
account = Apka()
response = account.signIn()

chars = account.chars()

#only for test
for i in chars:
    print(i)