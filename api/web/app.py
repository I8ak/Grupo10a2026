from flask import Flask, jsonify, request
from funciones_auxiliares import sanitize_field
import os
from funciones_auxiliares import prepare_response_extra_headers 
from flask_wtf.csrf import CSRFProtect 

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DB_HOST=os.getenv('DB_HOST'),
        DB_USER=os.getenv('DB_USER'),
        DB_PASSWORD=os.getenv('DB_PASSWORD'),
        DB_NAME=os.getenv('DB_NAME'),
        DB_PORT=os.getenv('DB_PORT', '3306'),
        WTF_CSRF_ENABLED=False
    )
    
    #app.config.from_pyfile('settings.py')
    csrf.init_app(app)
    
    #Configuración de la cabecera
    extra_headers=prepare_response_extra_headers(True)
    #Configuración de las sesiones con cookies
    app.config.update(PERMANENT_SESSION_LIFETIME=600)
    #app.config.update( SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',) #CON HTTPS
    app.config.update( SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)  # CON HTTP

    @app.before_request
    def clean_request():
        if request.is_json:
            # Guardamos los datos ya limpios en un nuevo atributo del objeto request
            request.cleaned_json = sanitize_field(request.get_json())


    
    app.config['DEBUG'] = False
    # configuración...
    app.config.setdefault('DEBUG', True)

    # Importar y registrar blueprints aquí (evita side-effects en import)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    csrf.exempt('rutas_usuarios.bp')
    from rutas_perfumes import bp as perfumes_bp
    app.register_blueprint(perfumes_bp, url_prefix='/api/perfumes')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.errorhandler(500)
    def server_error(error):
        print('An exception occurred during a request. ERROR:' + error, flush=True)
        ret={"status": "Internal Server Error"}
        return jsonify(ret), 500

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Obtenemos las variables con valores de respaldo (fallback)
    env_port = os.environ.get('PORT', '5000')
    env_host = os.environ.get('HOST', '0.0.0.0')
    
    try:
        port = int(env_port)
        print(f"Intentando arrancar en {env_host}:{port}...", flush=True)
        app.run(host=env_host, port=port)
    except Exception as e:
        print(f"FALLO CRÍTICO: No se pudo arrancar el servidor. Puerto configurado: {env_port}")
        print(f"Error detallado: {e}", flush=True)
