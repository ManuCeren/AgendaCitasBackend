from flask import Flask 
from flask_cors import CORS
from config.config import app_config

from apis.pacientes.routes import Paciente
from apis.citas.routes import Cita
from apis.telefonos.routes import Telefono
from apis.notificaciones.routes import Notificacion

def create_app():

    # Crear una instancia de aplicacion Flask 
    app = Flask(__name__)

    # Habilitar CORS para todas las rutas y origenes 
    # Esto permite que el frontend realice solicitudes a la Api
    CORS(app, supports_credentials=True, origins="*")
    app.config.from_object(app_config['development'])

    #apartado para las rutas 
    app.register_blueprint(Paciente.paciente_bd, url_prefix="/api/pacientes")
    app.register_blueprint(Cita.main, url_prefix="/api/citas")
    app.register_blueprint(Telefono.main, url_prefix="/api/telefonos")
    app.register_blueprint(Notificacion.main, url_prefix="/api/notificaciones")


   # Manejo de errores
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return "<h1>Página no encontrada</h1>", 404

    @app.errorhandler(500)
    def error_servidor(error):
        return "<h1>Error interno del servidor</h1>", 500
    
    #@app.route("/cors-debug")
    #def cors_debug():
        #return "CORS Debug OK"

    @app.route('/')
    def principal():
        return "<h1>Bienvenido a mi aplicacion con Flask</h1>" 
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)