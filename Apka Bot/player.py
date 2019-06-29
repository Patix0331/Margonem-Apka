import apka

class Player:
    def ChooseCharacters(self):
        while True:
            charnumber = input("By wystartować bota kliknij ENTER! Wprowadź numer postaci do expienia:  ")
            if charnumber == "" :
                break
            else:
                try:
                    charnumber = int(charnumber)
                    charnumbers.append(charnumber)
                except Exception:
                    print("By wystartować bota kliknij ENTER")
                    continue

        return charnumbers