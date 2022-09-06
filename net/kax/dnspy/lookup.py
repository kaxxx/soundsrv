import socket
import os
import ipaddress
import json
import time

from playsound import playsound

class Lookup:

    clients_available = {}
    clients_online = {}
    soundmapping = {}

    def __init__(self):
        self.load_soundmapping()

    def load_soundmapping(self):
        # read file
        with open('./uploads/soundmapping.json', 'r') as myfile:
            data = myfile.read()
        myfile.close()
        self.soundmapping = json.loads(data)
        return self.soundmapping

    def update_soundmapping(self):
        filename = './uploads/soundmapping.json'
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
        return True if os.system("ping -c 2 " + str(SOMEHOST).strip(";") + " >/dev/null 2>&1") == 0 else False

    def remove_domain(self, data):
        resp = {}
        for (k, v) in data.items():
            print("key: "+str(k))
            print("value: "+str(v).split('.')[0])
            resp[str(v.split('.')[0])] = k
        return resp

    def check_sound(self):
        #TODO: If new upload comes in during processing, it will be overwritten by
        #TODO: update_soundmapping() later in this method. -> Make a reliable persistance
        clients = dict(self.load_soundmapping())
        print("clients soundmapping: "+str(len(clients)))
        #print(clients)
        if len(clients) == 0:
            time.sleep(3000)
            return
        for key, value in clients.items():
            #print("sound: "+clients[key]['sound'])
            print(str(key)+" - sound:"+str(clients[key]['sound'])+" ... try to ping!")
            if self.checkonline(key) and clients[key]['played'] == False:
                print("***** SOUND: "+clients[key]['sound']+" *****")
                try:
                    playsound(clients[key]['sound'])
                    clients[key]['played'] = True
                except:
                    print("ERROR playing sound: "+clients[key]['sound'])

            elif self.checkonline(key) == False:
                print(key+" not reachable, no play needed and set sound flag to False.")
                clients[key]['played'] = False
            else:
                print(key+" sound was already played.")

        self.soundmapping = clients
        self.update_soundmapping()

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
