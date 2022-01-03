from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run()

