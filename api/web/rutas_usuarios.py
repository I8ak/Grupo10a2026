from __future__ import print_function
from flask import request, Blueprint, jsonify, make_response
from funciones_auxiliares import Encoder
import controlador_usuarios
import json

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'], strict_slashes=False)
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.cleaned_json
        if login_json and "username" in login_json and "password" in login_json:
            username = login_json['username']
            password = login_json['password']
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.login_usuario(username, password)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 401
        else:
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return make_response(jsonify(respuesta), code)

@bp.route("/registro", methods=['POST'], strict_slashes=False)
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.cleaned_json
        username = login_json['username']
        password = login_json['password']
        profile = login_json['profile']
        respuesta, code = controlador_usuarios.alta_usuario(username, password, profile)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return make_response(jsonify(respuesta), code)


@bp.route("/logout",methods=['GET'])
def logout():
    try:
        controlador_usuarios.logout()
        ret = {"status": "OK"}
        code = 200
    except:
        ret = {"status": "ERROR"}
        code = 500
        response=make_response(json.dumps(ret),code)
    return response

