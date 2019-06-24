class Characters:
    
    name = []
    id = []
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
        for char in characters:

            Character_List = Characters()
            Character_List.name.append(char[0])
            Character_List.id.append(char[1])

        return Character_List

        
account = Apka()
response = account.signIn()
<<<<<<< HEAD
=======
<<<<<<< HEAD
characters = account.chars()
#just checking if i can edit
=======
<<<<<<< HEAD
characters = account.chars()
#just checking if i can edit
=======
>>>>>>> parent of 0323933... making code human-readable xd
>>>>>>> wtf
chars = account.chars()

print(response.cookies, "\n")
chars = list(zip(chars.name, chars.id))
print(chars)
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> 0186a6ee7b5e831803623e31a440dce798b8c421
>>>>>>> parent of 0323933... making code human-readable xd
#stop updating now xd
>>>>>>> wtf
