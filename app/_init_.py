
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    from app.routes.categorias import bp as categorias_bp
    from app.routes.productos import bp as productos_bp
    from app.routes.meseros import bp as meseros_bp
    from app.routes.ordenes import bp as ordenes_bp
    from app.routes.detalles import bp as detalles_bp

    app.register_blueprint(categorias_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(meseros_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(detalles_bp)

    @app.route('/')
    def inicio():
        return render_template('index.html')

    return app
