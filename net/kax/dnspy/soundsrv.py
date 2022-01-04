from lookup import Lookup
from service import upload
from flask import Flask, render_template, request
from  multiprocessing import Process

soundmapping = {}

def subprocess():
    upload.start_srv()

Process(target=subprocess).start()


#upload.set_soundmapping(soundmapping)

print(".... start lookup")
lookup = Lookup()
while True:
    lookup.load_soundmapping()
    lookup.check_sound()
    print("... next try...")

