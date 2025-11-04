from flask import Flask
from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()  

class Professor(db.Model):
    __tablename__ = 'professores'
    id_professores = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    num_contrato = db.Column(db.String(20), nullable=False)
    lotacao = db.Column(db.String(100), nullable=False)
    cargo_funcao = db.Column(db.String(100), nullable=False)

class Cursos(db.Model):
    __tablename__ = 'cursos'
    id_cursos = db.Column(db.Integer, primary_key=True)
    nome_curso = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    palestrante = db.Column(db.String(100), nullable=False)

class Certificados(db.Model):
    __tablename__ = 'certificados'
    id_certificados = db.Column(db.Integer, primary_key=True)
    id_professores = db.Column(db.Integer, db.ForeignKey('professores.id_professores'), nullable=False)
    id_cursos = db.Column(db.Integer, db.ForeignKey('cursos.id_cursos'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    certificado_url = db.Column(db.String(200), nullable=True)
    carga_horaria_total = db.Column(db.Integer, nullable=False)

#Relacionamentos
    professor = db.relationship('Professor', backref='certificados')
    curso = db.relationship('Cursos', backref='certificados')