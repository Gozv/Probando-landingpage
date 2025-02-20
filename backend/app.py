from flask import Flask, render_template
from flask_cors import CORS
from backend.config import Config
from backend.models import db
from backend.routes.api import api
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Límites específicos
    limiter.limit("10/minute")(api.blueprint)

def create_app():
    app = Flask(__name__, 
                static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATES_FOLDER)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    
    # Routes
    @app.route('/')
    def home():
        return render_template('door.html')
    
    @app.route('/portfolio')
    def portfolio():
        return render_template('landing.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()

