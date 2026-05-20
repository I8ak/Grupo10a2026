import decimal
import json
import html
import bleach 
import bcrypt
import datetime


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

    
def calcularIVA(importe):
        return importe * 1.21
    

def sanitize_field(data):
    if isinstance(data, str):
        return bleach.clean(html.escape(data))
    if isinstance(data, dict):
        return {k: sanitize_field(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_field(v) for v in data]
    return data

def cipher_password(password):
  hashAndSalt = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))
  return hashAndSalt
def compare_password(password_hash,password):
   if password_hash is None:
      return False
   try:
      return bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8"))
   except:
      return False
  

from werkzeug.http import http_date

def prepare_response_extra_headers(include_security_headers):

    response_extra_headers = {
        # always
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
        'Server':''
    }
    if include_security_headers:
        response_security_headers = {
            # X-Frame-Options: page can only be shown in an iframe of the same site
            'X-Frame-Options': 'SAMEORIGIN',
            # ensure all app communication is sent over HTTPS
            'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
            # instructs the browser not to override the response content type
            'X-Content-Type-Options': 'nosniff',
            # enable browser cross-site scripting (XSS) filter
            'X-XSS-Protection': '1; mode=block'
        }
        response_extra_headers.update(response_security_headers)

    return response_extra_headers

from flask import session

def create_session(usuario,perfil):
    session["usuario"]=usuario
    session["perfil"]=perfil
def delete_session():
    session.clear()
def validar_session_normal():
    try:
        print(f"[DEBUG AUX] Validando sesión. Usuario en dict: {session.get('usuario')}", flush=True)
        # .get() devuelve None si la clave no existe, evitando el KeyError
        usuario = session.get("usuario")
        if usuario and usuario != "":
            return True
        return False
    except Exception as e:
        print(f"[DEBUG AUX] Error en validar_session_normal: {e}", flush=True)
        return False
def validar_session_admin():
    try:
        if (session["usuario"] and session["usuario"]!="" and session["perfil"]=="admin"):
            return True
        else:
            return False
    except:
        return False