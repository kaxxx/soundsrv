import socket
import os
import ipaddress
import json
import time

from playsound import playsound

class Lookup:

    clients_available = {}
    clients_online = {}

    def __init__(self):
        self.load_soundmapping()

    def load_soundmapping(self):
        # read file
        with open('/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/soundmapping.json', 'r') as myfile:
            data = myfile.read()
        self.soundmapping = json.loads(data)

    def update_soundmapping(self):
        filename = '/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/soundmapping.json'
        with open(filename, 'w') as f:
            json.dump(self.soundmapping, f)
        f.close()

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
            hostname = self.namebyip(ip)
            if hostname != "unknown":
                self.clients_available[hostname] = str(ip)
            ip = ip + 1

    def ping_available(self):
        for hostname, ip in self.clients_available.items():
            if self.checkonline(ip):
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
        if len(clients) == 0:
            #time.sleep(3000)
            return
        for key, value in clients.items():
            print("sound: "+value['sound'])
            print(str(key)+": "+str(value['sound']))
            if self.checkonline(key) and value['played'] == False:
                print("***** SOUND: "+value['sound']+" *****")
                playsound(value['sound'])
                self.soundmapping[key]['played'] = True
                self.update_soundmapping()
            elif self.checkonline(key) == False:
                self.soundmapping[key]['played'] = False
                self.update_soundmapping()
        json.dumps(clients)

    def get_clients_hdd(self):
        f = open('./clients_available.json')
        data = json.load(f)
        f.close()
        return data

#lookup = Lookup()

#clients = lookup.scan()
#print("clients found:",len(lookup.getAvailable()))

#lookup.ping_available()

#lookup.check_sound()
