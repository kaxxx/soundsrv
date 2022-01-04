import socket
import os
import ipaddress
import json
from playsound import playsound

class Lookup:

    clients_available = {}
    clients_online = {}
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

    def getAvailable(self):
        return self.clients_available

    def getOnline(self):
        return self.clients_online

    def namebyip(self, ip):
        hostinfo = ['none']
        try:
            hostinfo = socket.gethostbyaddr(str(ip))
        except socket.error as e:
            #print ("Error creating socket: %s" % e)
            hostinfo[0]="unknown"
        return hostinfo[0]

    def scan(self):
        ip = ipaddress.IPv4Address('192.168.2.1')
        ipmax = ipaddress.IPv4Address('192.168.2.255')
        while (ip <= ipmax):
            hostname = lookup.namebyip(ip)
            if hostname != "unknown":
                self.clients_available[hostname] = str(ip)
            ip = ip + 1

    def ping_available(self):
        for hostname, ip in self.clients_available.items():
            if lookup.checkonline(ip):
                self.clients_online[hostname] = str(ip)
        self.write_online()

    def write_online(self):
        json_obj = json.dumps(self.clients_online)
        file = open('clients_available.json', 'w',encoding="utf-8")
        file.write(json_obj)
        file.close()

    def checkonline(self, SOMEHOST):
        return True if os.system("ping -c 1 " + str(SOMEHOST).strip(";") + " >/dev/null 2>&1") == 0 else False

    def remove_domain(self, data):
        resp = {}
        for (k, v) in data.items():
            print("key: "+str(k))
            print("value: "+str(v).split('.')[0])
            resp[str(v.split('.')[0])] = k
        return resp

    def check_sound(self):
        clients = self.soundmapping
        print("clients soundmapping: "+str(len(clients)))
        print(clients)
        for key, value in clients.items():
            print("sound: "+value['sound'])
            print(str(key)+": "+str(value['sound']))
            if self.checkonline(key) and value['played'] == False:
                print("***** SOUND: "+value['sound']+" *****")
                playsound(value['sound'])
                self.soundmapping[key]['played'] = True
            elif self.checkonline(key) == False:
                self.soundmapping[key]['played'] = False
        json.dumps(clients)

    def get_clients_hdd(self):
        f = open('./clients_available.json')
        data = json.load(f)
        f.close()
        return data

lookup = Lookup()

#clients = lookup.scan()
#print("clients found:",len(lookup.getAvailable()))

#lookup.ping_available()

lookup.check_sound()
