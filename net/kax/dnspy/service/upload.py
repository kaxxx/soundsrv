from flask import Flask, render_template, request
from flask_classful import FlaskView
import json
import socket
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads' #os.path.abspath("./uploads")

app.config['MAX_CONTENT_PATH'] = 9999999
app.soundmapping = {}


def set_soundmapping(soundmappig):
    app.soundmapping = soundmappig
    print("****** GOT SOUNGMAPPING ******"+str(app.soundmapping))

@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/stylesheet')
def stylesheet():
    return render_template('css/style.css')


@app.route('/findhost')
def findhost():
    return render_template('js/upload.js')


@app.route('/jquery')
def jquery():
    return render_template('js/jquery-3.6.0.min.js')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        n = request.form['name']
        filename = "/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/" + n + ".mp3"
        print(filename)
        f.save(filename)
        do_soundmapping(n, filename)
        return render_template('uploaded.html')
    else:
        return render_template('error.html')

def load_soundmapping():
    # read file
    with open('/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/soundmapping.json', 'r') as myfile:
        data = myfile.read()
        return json.loads(data)

def do_soundmapping(name, filename):
    mapping  = load_soundmapping()
    new_element = {}
    new_element['sound'] = filename
    new_element['played'] = False
    #if name in new_mapping:
    #    print(name+" exists!")
    #else:
    mapping[name] = new_element
    app.soundmapping = mapping
    print(app.soundmapping)
    filename = "/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/uploads/soundmapping.json"
    with open(filename, 'w') as f:
        json.dump(app.soundmapping, f)
    f.close()

@app.route('/clients', methods=['GET'])
def get_clients():
    f = open('/home/kax/IdeaProjects/DNSPy/net/kax/dnspy/clients_available.json')
    data = json.load(f)
    f.close()
    return data


def remove_domain(data):
    resp = {}
    for (v, k) in data.items():
        print(str(k).split('.')[0])
        resp[str(k).split('.')[0]] = v
    return resp


@app.route('/hostname', methods=['GET'])
def get_hostname():
    ip = request.remote_addr
    name = socket.gethostbyaddr(ip)

    return name[0]

def get_soundmappig():
    return app.soundmapping

def start_srv():
    app.run(host='0.0.0.0')
    app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run()
