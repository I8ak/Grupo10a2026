from __future__ import print_function
from flask import request,Blueprint, jsonify, make_response
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):
        datos_limpos = request.cleaned_json
        if "usuario" in datos_limpos and "descripcion" in datos_limpos:
            usuario = datos_limpos['usuario']
            descripcion = datos_limpos['descripcion']
            if isinstance(usuario, str) and isinstance(descripcion, str) and len(usuario) < 100 and len(descripcion) < 500:
                respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
            else:
                respuesta = {"status": "Bad parameters", "mensaje": "Usuario o descripción demasiado largos"}
                code = 401
        else:
            respuesta = {"status": "Bad request", "mensaje": "Faltan campos 'usuario' o 'descripcion'"}
            code = 401
    else:
        respuesta={"status":"Bad request"}
        code=401
    return make_response(jsonify(respuesta), code)

@bp.route("/",methods=['GET'])
def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    return make_response(jsonify(respuesta), code)



