from flask import request, Blueprint, jsonify
import controlador_perfumes
from funciones_auxiliares import Encoder

bp = Blueprint('perfumes', __name__)

@bp.route("/",methods=["GET"])
def perfumes():
    respuesta,code= controlador_perfumes.obtener_perfumes()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def perfume_por_id(id):
    respuesta,code = controlador_perfumes.obtener_perfume_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_perfume():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        perfume_json = request.json
        nombre = perfume_json["nombre"]
        descripcion = perfume_json["descripcion"]
        precio = perfume_json["precio"]
        foto=perfume_json["foto"]
        notas=perfume_json["notas"]
        respuesta,code=controlador_perfumes.insertar_perfume(nombre, descripcion,precio,foto,notas)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_perfume(id):
    respuesta,code=controlador_perfumes.eliminar_perfume(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_perfume():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        perfume_json = request.json
        id = perfume_json["id"]
        nombre = perfume_json["nombre"]
        descripcion = perfume_json["descripcion"]
        precio=float(perfume_json["precio"])
        foto=perfume_json["foto"]
        notas=perfume_json["notas"]
        respuesta,code=controlador_perfumes.actualizar_perfume(id,nombre,descripcion,precio,foto,notas)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

