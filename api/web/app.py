from flask import Flask, jsonify
import os
from variables import cargarvariables

def create_app():
    app = Flask(__name__)

    # configuración...
    app.config.setdefault('DEBUG', True)

    # Importar y registrar blueprints aquí (evita side-effects en import)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

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
