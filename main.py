from flask import Flask, request, jsonify, send_file, redirect, make_response, url_for, render_template, Response, abort, session
from flask_cors import CORS
import json
import requests
import os
import uuid

name = f"{__name__}.py"

app = Flask(__name__)
app.config["SECRET_KEY"] = "PLS DO NOT KEEP THIS"
CORS(app)

dbPath = ""#* Example "C:\\ZestRec\\db\\""
cdnPath = ""#* Example "C:\\ZestRec\\cdn\\""
recRoomCdnUrl = "https://cdn.rec.net/"


@app.errorhandler(404)
def q405(e):
    data = ""
    return data, 404

@app.errorhandler(405)
def q405(e):
    data = ""
    return data, 405

@app.errorhandler(401)
def q401(e):
    data = ""
    return data, 401

@app.errorhandler(403)
def q403(e):
    data = ""
    return data, 403

@app.errorhandler(500)
def q405(e):
    data = {"Message":"An error has occurred."}
    return jsonify(data), 500

@app.route("/", methods=["GET"])
def index():
    return abort(404)

@app.route("/config/LoadingScreenTipData", methods=["GET"])
def config_LoadingScreenTipData(): 
    with open(f"{dbPath}api\\loading.json") as f:
        data = json.load(f)
        return data

@app.route("/data/<DataBlob>", methods=["GET"])
def data(DataBlob):
    if os.path.exists(f"{cdnPath}data\\{DataBlob}"):
        try:
            return send_file(f"{cdnPath}data\\{DataBlob}")
        except:
            return abort(500)
    else:
        data22 = requests.get(f"{recRoomCdnUrl}data/{DataBlob}", headers={"User-Agent": "BestHTTP"})
        if data22.status_code != 200:
            return abort(404)
        with open(f"{cdnPath}data\\{DataBlob}", "wb") as F:
            F.write(data22.content)
        return Response(data22.content, 200, content_type="application/octet-stream")
    
@app.route("/video/<DataBlob>", methods=["GET"])
def video(DataBlob):
    if os.path.exists(f"{cdnPath}video\\{DataBlob}"):
        try:
            return send_file(f"{cdnPath}video\\{DataBlob}")
        except:
            return abort(500)
    else:
        return abort(404)
    
@app.route("/room/<DataBlob>", methods=["GET"])
def room(DataBlob):
    if os.path.exists(f"{cdnPath}room\\{DataBlob}"):
        try:
            return send_file(f"{cdnPath}room\\{DataBlob}")
        except:
            return abort(500)
    else:
        data22 = requests.get(f"{recRoomCdnUrl}room/{DataBlob}", headers={"User-Agent": "BestHTTP"})
        if data22.status_code != 200:
            return abort(404)
        with open(f"{cdnPath}room\\{DataBlob}", "wb") as F:
            F.write(data22.content)
        return Response(data22.content, 200, content_type="application/octet-stream")
    
@app.route("/sigs/<DataBlob>", methods=["GET"])
def sigs(DataBlob):
    return abort(404)
    if os.path.exists(f"{cdnPath}sigs\\{DataBlob}"):
        try:
            return send_file(f"{cdnPath}sigs\\{DataBlob}")
        except:
            return abort(500)
    else:
        return abort(404)
    
@app.route("/strings", methods=["GET"])
def Strings():
    return abort(404)
    
@app.route("/health", methods=["GET"])
def health():
    return jsonify("Healthy")

def run():
    Port = 8080
    Ip = "0.0.0.0"
    app.run(str(Ip), int(Port))
    #ssl_context='adhoc'

run()