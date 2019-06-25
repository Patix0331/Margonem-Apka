class Player:
    def __init__(self, id, nick, world, cookies):
        self.id = id
        self.nick = nick
        self.world = world
        self.cookies = cookies
        cookies.set("mchar_id", id)