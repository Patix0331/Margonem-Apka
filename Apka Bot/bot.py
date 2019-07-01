"""Main program"""
from apka import *
import player
from engine import *
def LogIntoBot(login, password):
    cokiess = signIn(login,password)
    print(cokiess)
    chars1 = chars(cokiess)
    userid = cokiess["user_id"]
    #chars: 0 - id, 1 - nick, 2 - lvl, 3 - prof, 4 - world, 5 - stamina
    def postki():
        c = 0
        ret = []
        for i in chars1:
            ret.append((i[1] + " (" + i[2] + i[3] + ") [" + i[4] + "] - " + i[0] +" pozostało " + i[5] + " staminy " + "NUMER POSTACI:" + str(c) + "\n"))
            c += 1
        return ret
    postki1 = postki()
    return postki1, userid, cokiess, chars1
def RunBot(chosen):
    engine = Engine(userid, cokiess, chars1, chosen)
    engine.Run()

y, userid, cokiess, chars1 = LogIntoBot("app","1234")
print(y)
x = RunBot([0,1,2])
print(x)
#engine.Engine()
#print(chars)
#apk = apka.apka()

#response = apk.signIn()
#apk.chars(response)