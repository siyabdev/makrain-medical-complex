from flask import Flask
from database import init_db
from flask_cors import CORS
from config import Config

#Login class controller
from controller.login.login import login_bp

#Employee class controller
from controller.employee.create import employee_create_bp
from controller.employee.delete import employee_delete_bp
from controller.employee.get import employee_get_bp
from controller.employee.update import employee_update_bp

#Patient class controller
from controller.patient.create import patient_create_bp
from controller.patient.delete import patient_delete_bp
from controller.patient.get import patient_get_bp
from controller.patient.update import patient_update_bp

#Report class controller
from controller.report.create import report_create_bp
from controller.report.delete import report_delete_bp
from controller.report.get import report_get_bp
from controller.report.update import report_update_bp

#Ward class controller
from controller.ward.create import ward_create_bp
from controller.ward.delete import ward_delete_bp
from controller.ward.get import ward_get_bp
from controller.ward.update import ward_update_bp

def create_app():
    app = Flask(__name__)

    #Loading configuration
    app.config.from_object(Config)

    #CORS
    CORS(app)

    #Logging
    app.logger.setLevel(app.config["LOG_LEVEL"])

    #Initialize database
    init_db(app)

    #Blueprints

    #Login class
    app.register_blueprint(login_bp)

    #Employee class
    app.register_blueprint(employee_create_bp)
    app.register_blueprint(employee_delete_bp)
    app.register_blueprint(employee_get_bp)
    app.register_blueprint(employee_update_bp)

    #Patient class
    app.register_blueprint(patient_create_bp)
    app.register_blueprint(patient_delete_bp)
    app.register_blueprint(patient_get_bp)
    app.register_blueprint(patient_update_bp)

    #Report class
    app.register_blueprint(report_create_bp)
    app.register_blueprint(report_delete_bp)
    app.register_blueprint(report_get_bp)
    app.register_blueprint(report_update_bp)

    #Ward class
    app.register_blueprint(ward_create_bp)
    app.register_blueprint(ward_delete_bp)
    app.register_blueprint(ward_get_bp)
    app.register_blueprint(ward_update_bp)

    @app.route("/")
    def Home():
        return "Welcome To Flask"
    
    return app

#Run FlasK
app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)