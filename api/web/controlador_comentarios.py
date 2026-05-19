from bd import obtener_conexion
import sys
import datetime as dt
from funciones_auxiliares import sanitize_field


def convertir_comentario_a_json(comentario):
    return{
        'id': comentario[0],
        'usuario': sanitize_field(comentario[1]),
        'descripcion': sanitize_field(comentario[2])
    }

def insertar_comentario(usuario, descripcion):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)"
            cursor.execute(query, (usuario, descripcion))
            conexion.commit()
        conexion.close()
        ret={"status": "OK" }
        code=200
    except:
        ret={"status": "ERROR" }
        print("Excepcion al insertar un comentario", flush=True)
        code=500   
    return ret,code

def obtener_comentarios():
    comentariosjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas los comentarios", flush=True)
        code=500
    finally:
        if conexion:
            conexion.close()
    return comentariosjson,code