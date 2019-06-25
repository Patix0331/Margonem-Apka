"""Main program"""
import apka
import engine
import player

apk = apka.Apka()

response = apk.signIn()
apk.chars(response)