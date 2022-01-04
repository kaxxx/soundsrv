from lookup import Lookup
from service import upload

soundmapping = {
    'iPad.fritz.box': {
        'sound': '/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/Pixel-4a.fritz.box.mp3',
        'played': False
    },
    'kay-P10-2.fritz.box': {
        'sound': '/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/kay-P10-2.fritz.box.mp3',
        'played': False
    }
}

lookup = Lookup(soundmapping)
while True:
    lookup.check_sound()

