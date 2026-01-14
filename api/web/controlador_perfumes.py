from bd import obtener_conexion
import sys


def convertir_chuche_a_json(chuche):
    d = {}
    d['id'] = chuche[0]
    d['nombre'] = chuche[1]
    d['descripcion'] = chuche[2]
    d['precio'] = float(chuche[3])
    d['foto'] = chuche[4]
    d['notas']=chuche[5]
    return d

def insertar_chuche(nombre, descripcion, precio,foto,notas):
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
                for chuche in perfumes:
                    perfumesjson.append(convertir_chuche_a_json(chuche))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las perfumes", flush=True)
        code=500
    return perfumesjson,code

def obtener_chuche_por_id(id):
    chuchejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,notas FROM perfumes WHERE id =" + id)
            chuche = cursor.fetchone()
            if chuche is not None:
                chuchejson = convertir_chuche_a_json(chuche)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una chuche", flush=True)
        code=500
    return chuchejson,code
def eliminar_chuche(id):
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
        print("Excepcion al eliminar una chuche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_chuche(id, nombre, descripcion, precio, foto,notas):
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
        print("Excepcion al actualziar una chuche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code
