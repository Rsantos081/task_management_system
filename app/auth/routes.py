from flask import request, jsonify
from flask_login import login_user, logout_user

from app.auth import auth_bp
from app.extensions import db
from app.models import Usuario


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Usuario.query.filter_by(nome=data.get("nome")).first()

    if user and data.get("senha") == user.senha:
        login_user(user)
        return jsonify({"mensagem": "Usuario Autenticado com Sucesso"})

    return jsonify({"mensagem": "Credencias Invalidas do Usuario"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"mensagem": "Logout Realizado com Sucesso"})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if 'nome' in data and 'senha' in data:
        if Usuario.query.filter_by(nome=data["nome"]).first():
            return jsonify({"mensagem": "Usuario ja existe"}), 400
        usuario = Usuario(nome=data["nome"], senha=data["senha"])
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuario Cadastrado com Sucesso"}), 200
    return jsonify({"mensagem": "Dados Invalidos do Usuario"}), 400
