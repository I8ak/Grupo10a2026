from bd import obtener_conexion
import sys
from funciones_auxiliares import calcularIVA


def convertir_perfume_a_json(perfume):
    d = {}
    d['id'] = perfume[0]
    d['nombre'] = perfume[1]
    d['descripcion'] = perfume[2]
    d['precio'] = float(perfume[3])
    d['foto'] = perfume[4]
    d['notas']=perfume[5]
    return d

def insertar_perfume(nombre, descripcion, precio,foto,notas):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO perfumes(nombre, descripcion, precio,foto,notas) VALUES (%s, %s, %s,%s,%s)",
                       (nombre, descripcion, precio,foto,notas))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_perfumes():
    perfumesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,notas FROM perfumes")
            perfumes = cursor.fetchall()
            if perfumes:
                for perfume in perfumes:
                    perfumesjson.append(convertir_perfume_a_json(perfume))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las perfumes", flush=True)
        code=500
    return perfumesjson,code

def obtener_perfume_por_id(id):
    perfumejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,notas FROM perfumes WHERE id =" + id)
            perfume = cursor.fetchone()
            if perfume is not None:
                perfumejson = convertir_perfume_a_json(perfume)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una perfume", flush=True)
        code=500
    return perfumejson,code
def eliminar_perfume(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM perfumes WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una perfume", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_perfume(id, nombre, descripcion, precio, foto,notas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE perfumes SET nombre = %s, descripcion = %s, precio = %s, foto=%s, notas=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,notas,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualziar una perfume", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code
