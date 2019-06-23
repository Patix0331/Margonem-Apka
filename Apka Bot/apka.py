class Apka:
    import hashlib
    login = input("Podaj login: ").encode('ascii')
    password = input("Podaj hasło: ").encode('ascii')
    hash = hashlib.sha1
    hashed_password = hash(b"mleczko"+password).hexdigest()

    def loging(self, login=login, ph=hashed_password):
        import requests
        response = requests.post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
            'l': login,
            'ph': ph
        })
        if("logged" in str(response.content)):
            return response
        else:
            raise Exception

log = Apka()
response = log.loging()
print(response.cookies)
