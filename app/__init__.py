from flask import Flask

def create_app():
    """
    App Factory: patrón recomendado.
    Permite crear la app con configuración limpia y testear fácilmente.
    """
    app = Flask(__name__)

    # Config básica (si necesitas variables, aquí o desde un archivo .env/config)
    app.config["SECRET_KEY"] = "dev"  # para sesiones/CSRF si luego usamos formularios

    # Registrar rutas en un módulo separado
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

