from flask_login import UserMixin
from app.extensions import db


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    tarefas = db.relationship('Tarefas', backref='usuario', lazy=True)


class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(99), nullable=False)
    descricao = db.Column(db.String(99), nullable=False)
    status = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
