from bd import obtener_conexion
import sys
import datetime as dt
from flask import current_app as app
from funciones_auxiliares import cipher_password, compare_password, create_session
from flask_wtf.csrf import generate_csrf

def login_usuario(username,password):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT perfil, clave, numeroAccesosErroneo FROM usuarios WHERE estado='activo' AND usuario = %s",
                (username,)
            )
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                ret = {"status": "OK" }
                
            perfil,password_hash, num_erroneos = usuario
            hoy =dt.date.today().strftime("%Y-%m-%d")
            
            if compare_password(password, password_hash):
                ret = {
                    "status": "OK",
                    "perfil": perfil,
                    "csrf_token": generate_csrf()
                }
                create_session(username, perfil)
                app.logger.info("Acceso correcto: Usuario %s", username)
                create_session(username, perfil)
                cursor.execute(
                    "UPDATE usuarios SET numeroAccesosErroneo=0, fechaUltimoAcceso=%s, estado='activo' WHERE usuario = %s",
                    (hoy, username)
                )
                conexion.commit()
                return ret, 200
            else:
                num_erroneos += 1
                estado = 'bloqueado' if num_erroneos > 2 else 'activo'
                cursor.execute(
                    "UPDATE usuarios SET numeroAccesosErroneo=%s, estado=%s WHERE usuario = %s",
                    (num_erroneos, estado, username)
                )
                conexion.commit()
                ret = {
                    "status": "ERROR",
                    "mensaje": "Usuario/clave erroneo"
                }
    except:
        print("Excepcion al validar al usuario", flush=True)   
        ret={"status":"ERROR"}
        code=500
    finally:
        if conexion:
            conexion.close()
    return ret,200

def alta_usuario(username,password,perfil):
    conexion = None
    # Inicializamos valores por si acaso
    ret = {"status": "ERROR"}
    code = 500
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
            if cursor.fetchone() is not None:
                return {"status": "ERROR", "mensaje": "Usuario ya existe"}, 200
            password_hash = cipher_password(password)
            query = """
                INSERT INTO usuarios(usuario, clave, perfil, estado, numeroAccesosErroneo) 
                VALUES (%s, %s, %s, 'activo', 0)
            """
            cursor.execute(query, (username, password_hash, perfil))
            if cursor.rowcount == 1:
                conexion.commit()
                app.logger.info("Nuevo usuario creado: %s", username)
                return {"status": "OK"}, 200
            
            return {"status": "ERROR"}, 500
    except:
        print("Excepcion al registrar al usuario", flush=True)   
        ret={"status":"ERROR"}
        code=500
    finally:
        if conexion:
            conexion.close()
    return ret,code    

def logout():
    return {"status":"OK"},200


