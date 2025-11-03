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

class Formacoes(db.Model):
    __tablename__ = 'formacoes'
    id_formacoes = db.Column(db.Integer, primary_key=True)
    nome_formacao = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

class Certificados(db.Model):
    __tablename__ = 'certificados'
    id_certificados = db.Column(db.Integer, primary_key=True)
    id_professores = db.Column(db.Integer, db.ForeignKey('professores.id_professores'), nullable=False)
    id_formacoes = db.Column(db.Integer, db.ForeignKey('formacoes.id_formacoes'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    certificado_url = db.Column(db.String(200), nullable=True)
    carga_horaria_total = db.Column(db.Integer, nullable=False)

#Relacionamentos
    professor = db.relationship('Professor', backref='certificados')
    formacao = db.relationship('Formacoes', backref='certificados')