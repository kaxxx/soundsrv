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

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        n = request.form['name']
        f.save(app.config['UPLOAD_FOLDER']+"/"+n)
        return 'file uploaded successfully'

@app.route('/clients', methods = ['GET'])
def get_clients():
    f = open('../clients_available.json')
    data = json.load(f)
    f.close()
    remove_domain(data)
    return remove_domain(data)

def remove_domain(data):
    resp = {}
    for (k, v) in data.items():
        resp[str(k).split('.')[0]] = v
    return resp

@app.route('/hostname', methods = ['GET'])
def get_hostname():
    name = socket.gethostname()
    return name


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run()

