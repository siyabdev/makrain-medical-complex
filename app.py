from flask import Flask
from database import init_db
from flask_cors import CORS
from config import Config

#Importing Blueprints
from controller.login import login_bp
from controller.employee import employee_bp
from controller.patient import patient_bp
from controller.report import report_bp
from controller.ward import ward_bp

def create_app():
    app = Flask(__name__)

    #Loading config
    app.config.from_object(Config)

    #CORS
    CORS(app)

    #Logging
    app.logger.setLevel(app.config["LOG_LEVEL"])

    #Initialize database
    init_db(app)

    #Registering Blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(ward_bp)

    @app.route("/")
    def Home():
        return "Welcome To Flask"
    
    return app

#Run FlasK
app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)