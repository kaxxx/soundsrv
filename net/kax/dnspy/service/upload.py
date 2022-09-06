from flask import Flask, render_template, request
from flask_classful import FlaskView
import json
import socket
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads' #os.path.abspath("./uploads")

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
        filename = "../uploads/" + n + ".mp3"
        print(filename)
        f.save(filename)
        do_soundmapping(n, filename)
        return render_template('uploaded.html')
    else:
        return render_template('error.html')

def load_soundmapping():
    # read file
    with open('../uploads/soundmapping.json', 'r') as myfile:
        data = myfile.read()
    myfile.close()

    return json.loads(data)

def do_soundmapping(name, filename):
    mapping = {}

    mapping  = dict(load_soundmapping())
    print ("old mapping: "+str(mapping))
    new_element = {}
    new_element['sound'] = filename
    new_element['played'] = False

    if name in mapping.keys():
        print(name+" exists!")
    else:
        print(name+" NOT existing!")
    mapping[name] = new_element
    print ("new mapping: "+str(mapping))
    app.soundmapping = mapping

    filename = "../uploads/soundmapping.json"
    #json_object = json.dumps(app.soundmapping, indent = 4)
    with open(filename, 'w') as f:
        json.dump(app.soundmapping, f)
    f.close()


@app.route('/clients', methods=['GET'])
def get_clients():
    f = open('./clients_available.json')
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
    print(ip)
    try:
        name = socket.gethostbyaddr(ip)[0]
    except:
        name = ip

    return name

def get_soundmappig():
    return app.soundmapping

def start_srv():
    app.run(host='0.0.0.0')
    app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run()
