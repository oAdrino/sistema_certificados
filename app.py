from routes.professores import professores_bp
from routes.cursos import cursos_bp
from routes.certificados import certificados_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oAdrino:250866@localhost:5432/cursos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(professores_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(certificados_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)