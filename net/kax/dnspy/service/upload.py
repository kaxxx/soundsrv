from flask import Flask, render_template, request
import json
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../uploads/"
app.config['MAX_CONTENT_PATH'] = 9999999

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

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        n = request.form['name']
        f.save(app.config['UPLOAD_FOLDER']+"/"+n)
        return render_template('uploaded.html')
    else:
        return render_template('error.html')

@app.route('/clients', methods = ['GET'])
def get_clients():
    f = open('../clients_available.json')
    data = json.load(f)
    f.close()
    return data

def remove_domain(data):
    resp = {}
    for (v, k) in data.items():
        print(str(k).split('.')[0])
        resp[str(k).split('.')[0]] = v
    return resp

@app.route('/hostname', methods = ['GET'])
def get_hostname():
    ip = request.remote_addr
    name = socket.gethostbyaddr(ip)
    
    return name[0]



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run()

