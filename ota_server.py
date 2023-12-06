import hashlib
import os
import sys
import json
import shutil
from datetime import date
import logging
from flask import Flask, send_file, jsonify, request, render_template, redirect
 
app = Flask(__name__,template_folder='template')
app.config['MAX_CONTENT_PATH'] = 502000


logging.basicConfig(filename='devices_update.log', format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
logger=logging.getLogger()

ADDRESS_IP = 'https://lucadalessandro.tech'
PATH = "/home/luca/Projects/OTA-Server"

# ================================================

def read_json_file():
    with open(os.path.join(PATH, "device.json"),"r") as f:
        return json.load(f)


@app.route('/ota/api/post/update/<api_key>', methods=['GET','POST'])
def api_update_prova(api_key):
    API_TOKEN_LIST = read_json_file()
    if api_key in API_TOKEN_LIST:
        try:
            logger.info("{}: {} -> {}".format(api_key,request.headers['X-Esp8266-Version'],API_TOKEN_LIST[api_key]['version']))
        except Exception as e:
            logger.warning('request {} from non X-Esp8266 device'.format(api_key))
        try:
            return send_file(os.path.join(PATH,"firmware",api_key,API_TOKEN_LIST[api_key]['fileName']))
        except Exception as e:
                return str(e)
    

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
    return render_template('upload.html', devices=API_TOKEN_LIST, ip = ADDRESS_IP)


@app.route('/uploader', methods = ['GET', 'POST'])
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
    

@app.route('/favicon.ico')
def favicon():
    return send_file('./static/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='192.168.1.250', port=50001, debug=False)
