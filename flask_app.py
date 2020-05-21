
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, url_for
from flask import request
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin
import os, time
from os.path import join, dirname, realpath
import jsonpickle
import numpy as np
import cv2
app = Flask(__name__)
cors = CORS(app)
UPLOAD_FOLDER1 = join(dirname(realpath(__file__)), 'static/')
app.config['CORS_ORIGIN'] = '*'
app.config['CORS_METHODS'] = 'GET, POST, OPTIONS'
app.config['CORS_HEADERS'] = 'Content-Type, User-Agent'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1
app.config['JSON_ADD_STATUS'] = True
app.config['JSON_STATUS_FIELD_NAME'] = ''

ALLOWED_EXTENSIONS = {'JPG', 'PNG', 'JPEG', 'GIF', 'jpg', 'png', 'jpeg', 'gif'}
baseUrl = 'https://wiraoke300.pythonanywhere.com/'

os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()

@app.errorhandler(405)
def mna(e):
  return json.dumps({'statusCode':405, 'status':False, 'code':'01', 'message':'Method Not Allowed'}), 405, {'Content-Type':'application/json'}

@app.errorhandler(400)
def bdr(e):
  return json.dumps({'statusCode':400, 'status':False, 'code':'01', 'message':'Bad Request'}), 400, {'Content-Type':'application/json'}

@app.errorhandler(500)
def ise(e):
  return json.dumps({'statusCode':500, 'status':False, 'code':'01', 'message':'Internal Server Error'}), 500, {'Content-Type':'application/json'}

@app.errorhandler(404)
def not_found(e):
  return json.dumps({'statusCode':404, 'status':False, 'code':'01', 'message':'The resource could not be found'}), 404, {'Content-Type':'application/json'}

@app.route('/')
def hello_world():
    #return '''<b>Welcome to Wira Dwi Susanto's API</b>''';
    return redirect(url_for('upload_gambar'))

@app.route('/upload_gambar')
def upload_gambar():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    images = os.listdir(os.path.join(app.static_folder, ""))
    return render_template('gallery.html', images=images)

@app.route('/api')
def api():
    return '''<b>Welcome to Wira Dwi Susanto's API</b>''';

@app.route('/api/v1')
def apiv1():
    return '''<b>Welcome to Wira Dwi Susanto's API</b>''';

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/image_client_get', methods=['GET', 'OPTIONS'])
@cross_origin()
def image_client_get():
    images = os.listdir(os.path.join(app.static_folder, ""))
    jsonData = []
    id = 1
    for getImage in images:
        jsonData.append({'id':id, 'url':baseUrl + 'static/' + getImage})
        id += 1
    json_string = str(json.dumps(jsonData))
    json_string_encode = json.loads(json_string.replace("\'", '"'))
    return json.dumps({'statusCode':200, 'status':True, 'code':'00', 'message':'Berhasil menampilkan data gambar', 'data':json_string_encode}), 200, {'Content-Type':'application/json'}

@app.route('/api/image_upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def image_upload():
    waktuUpload = int(time.time())
    waktuUpload2 = str(waktuUpload)
    fileupload = request.files
    getGambar = fileupload['gambar']
    if allowed_file(getGambar.filename):
        filename = secure_filename(getGambar.filename)
        concatNamaFile = waktuUpload2 + '_' + filename
        getGambar.save(os.path.join(app.config['UPLOAD_FOLDER'], concatNamaFile))
        imgSrc = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], concatNamaFile))
        _, img_encoded = cv2.imencode('.jpg', imgSrc)
        dataImg=img_encoded.tostring()
        nparr = np.fromstring(dataImg, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
        response_pickled = jsonpickle.encode(response)
        return json.dumps({'statusCode':200, 'status':True, 'code':'00', 'message':'Upload sukses! ' + response_pickled}), 200, {'Content-Type':'application/json'}
    else:
         return json.dumps({'statusCode':200, 'status':False, 'code':'01', 'message':'Format gambar tidak didukung!'}), 200, {'Content-Type':'application/json'}

if __name__ == '__main__':
    app.run()