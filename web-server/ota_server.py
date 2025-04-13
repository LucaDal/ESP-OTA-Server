import hashlib
import os
import sys
import json
import shutil
from datetime import date
import logging
from dotenv import load_dotenv
from flask import Flask, send_file, jsonify, request, render_template, redirect, make_response
 
load_dotenv()

app = Flask(__name__,template_folder='template')
app.config['MAX_CONTENT_PATH'] = 502000

logging.basicConfig(filename='devices_update.log', format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.DEBUG)
logger=logging.getLogger()

PATH = os.getenv('PROJECT_PATH')

# ================================================

def read_json_file():
    with open(os.path.join(PATH, "device.json"),"r") as f:
        return json.load(f)


@app.route('/ota/api/post/update/<api_key>', methods=['GET','POST'])
def api_update_prova(api_key):
    API_TOKEN_LIST = read_json_file()
    if api_key in API_TOKEN_LIST:
        try:
            if('x-ESP8266-version' in request.headers):
                device = 'x-esp8266[{}]'.format(request.headers['x-ESP8266-STA-MAC'])  
                version = request.headers['x-ESP8266-version']
            if('x-ESP32-version' in request.headers):
                device = 'x-esp32[{}]'.format(request.headers['x-ESP32-STA-MAC'])
                version = request.headers['x-ESP32-version']
            logger.info("client [{}] - TOKEN [{}] - [{} -> {}]".format(device,api_key,version,API_TOKEN_LIST[api_key]['version']))
        except Exception as e:
            logger.warning('request {} from non x-esp device - error: {}'.format(api_key, e))
        try:
            with open(os.path.join(PATH,"firmware",api_key,API_TOKEN_LIST[api_key]['fileName']), "rb") as file_to_check:
                data = file_to_check.read()
                md5_returned = hashlib.md5(data).hexdigest()
            response = make_response(send_file(os.path.join(PATH,"firmware",api_key,API_TOKEN_LIST[api_key]['fileName'])))
            response.headers['x-MD5'] = md5_returned
            return response
        except Exception as e:
            logger.warning("Error sending file to {}".format(api_key))
    

def version(api_key, file_name, version):
    with open(os.path.join(PATH,"firmware",api_key,file_name), "rb") as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()
    value = {
        "version": version,
        "md5Checksum": md5_returned
    }
    return json.dumps(value)


@app.route('/ota/api/get/version/<api_key>')
def api_version(api_key):
    API_TOKEN_LIST = read_json_file() 
    if api_key in API_TOKEN_LIST:
        return version(api_key, API_TOKEN_LIST[api_key]['fileName'],API_TOKEN_LIST[api_key]['version'])
    else:
        return "none"


@app.route('/ota')
def upload_file():
    API_TOKEN_LIST = read_json_file() 
    return render_template('upload.html', devices=API_TOKEN_LIST)


@app.route('/ota/uploader', methods = ['GET', 'POST'])
def uploader_file():
    API_TOKEN_LIST = read_json_file()
    if request.method == 'POST':
        if request.form.get('button') == 'Delete':
            API_TOKEN_LIST.pop(request.form.get('token'))
            try:
                shutil.rmtree(os.path.join(PATH,"firmware",request.form.get('token')))
            except Exception as e:
                logger.warning('Error consistency in firmware folder')
        else:
            today = date.today()
            file = request.files['file']
            if file.filename[-4:] != '.bin':
                return 'File needed is .bin'
            if request.form.get('token') in API_TOKEN_LIST:
                API_TOKEN_LIST[request.form.get('token')]['version'] = request.form.get('version')
                API_TOKEN_LIST[request.form.get('token')]['buildDate'] = today.strftime("%d/%m/%Y")
                API_TOKEN_LIST[request.form.get('token')]['fileName'] = file.filename
            else:
                if not os.path.exists(os.path.join(PATH,"firmware",request.form.get('token'))):
                    
                    os.makedirs(os.path.join(PATH,"firmware",request.form.get('token')))
                    newJson = {request.form.get('token') : {
                        "companyName": "LucaLab",
                        "version": request.form.get('version'),
                        "buildDate": today.strftime("%d/%m/%Y"),
                        "fileName": file.filename
                        }
                    }
                    API_TOKEN_LIST.update(newJson)
            pathFile = 'firmware\\'+request.form.get('token')+'\\'+file.filename
            if os.path.exists(pathFile):
                os.remove(pathFile)
            os.chdir(os.path.join(PATH,"firmware",request.form.get('token')))
            file.save(file.filename)
        with open(os.path.join(PATH, "device.json"),"w") as f:
            json.dump(API_TOKEN_LIST,f,indent=4)
        return redirect("/ota")

if __name__ == '__main__':
    app.run(host='192.168.1.250', port=50001, debug=False)
