import socket
import os
import ipaddress
import json

class Lookup:

    clients_available={}
    clients_online={}
    soundmapping={'kay-P10-2.fritz.box':'/home/kax/Musik/Wischmeyer_Ostern.mp3'}

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
        for ip, hostname in self.clients_available.items():
            if lookup.checkonline(ip):
                self.clients_online[hostname] = str(ip)
        self.write_available()

    def write_available(self):
        json_obj = json.dumps(self.clients_available)
        file = open('clients_available.json', 'w',encoding="utf-8")
        file.write(json_obj)
        file.close()

    def checkonline(self, SOMEHOST):
        return True if os.system("ping -c 1 " + str(SOMEHOST).strip(";") + " >/dev/null 2>&1") == 0 else False

lookup = Lookup()

clients = lookup.scan()
print("clients found:",len(lookup.getAvailable()))

lookup.ping_available()

print("clients online: "+str(len(lookup.getOnline())))
for key, value in lookup.getOnline().items():
    print(str(key)+": "+str(value))
    if value in lookup.soundmapping:
        print("***** SOUND *****")
