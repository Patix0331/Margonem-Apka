import requests
import json

response = requests.post("https://www.margonem.pl/ajax/logon.php?t=login", data = {
    'l':'apkabot',
    'ph':'96f78d46bc3169599bffc3cdd16e2d843f31c55d'
})

id, server, nick = [], [], []

response = requests.post("http://www.margonem.pl/ajax/getplayerdata.php?app_version=1.3.3", cookies = response.cookies)
accounts = json.loads(response.text)

for char in accounts['charlist']:

    info = accounts['charlist'][char]
    world = (info['db'])[1:]

    id.append(info['id'])
    server.append(world)
    nick.append(info['nick'])
    
characters = list(zip(id,server,nick))

# for i in characters:
#     print(i)