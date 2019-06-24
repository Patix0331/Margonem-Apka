class Apka:
    import hashlib
    username = input("Podaj login: ").encode('ascii')
    password = input("Podaj hasło: ").encode('ascii')
    hash = hashlib.sha1
    hashed_password = hash(b"mleczko"+password).hexdigest()

    def signIn(self, username = username, ph=hashed_password):
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
            import re
            characters = re.findall(r"option label=\"(.*?)\" value=\"(.*?)\"", response.text)
            return characters

account = Apka()
response = account.signIn()
characters = account.chars()