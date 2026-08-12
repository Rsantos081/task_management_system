from flask import request, jsonify
from flask_login import login_required, current_user

from app.tasks import tasks_bp
from app.extensions import db
from app.models import Tarefas


@tasks_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def list_all_tasks():
    tarefas = Tarefas.query.filter_by(usuario_id=current_user.id).all()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "status": t.status
        } for t in tarefas
    ])


@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_tasks():
    data = request.json
    if 'titulo' in data and 'descricao' in data:
        tarefa = Tarefas(
            titulo=data["titulo"],
            descricao=data["descricao"],
            usuario_id=current_user.id
        )
        db.session.add(tarefa)
        db.session.commit()
        return jsonify({"mensagem": "Tarefa adicionada com sucesso"})
    return jsonify({"mensagem": "Dados invalido da Tarefa"}), 400


@tasks_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def remove_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id=current_user.id).first()
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
        return jsonify({"mensagem": "Tarefa removida com sucesso"})
    return jsonify({"mensagem": "Tarefa não encontrada Id invalido"}), 400


@tasks_bp.route('/<int:id>', methods=['GET'])
@login_required
def list_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id=current_user.id).first()
    if tarefa:
        return jsonify({
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "status": tarefa.status
        })
    return jsonify({"mensagem": "Tarefa não enontrado"}), 404


@tasks_bp.route('/update/<int:id>', methods=['PUT'])
@login_required
def update_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id=current_user.id).first()
    if not tarefa:
        return jsonify({"mensagem": "Tarefa não encontrada"}), 404
    data = request.json

    if 'titulo' in data:
        tarefa.titulo = data['titulo']

    if 'descricao' in data:
        tarefa.descricao = data['descricao']

    if 'status' in data:
        tarefa.status = data['status']
    db.session.commit()
    return jsonify({"mensagem": "Tarefa atualizada com sucesso"})


@tasks_bp.route('/<int:id>/completed', methods=['PATCH'])
@login_required
def mark_task_completed(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id=current_user.id).first()
    if not tarefa:
        return jsonify({"mensagem": "Tarefa não encontrada"}), 404
    data = request.json

    if 'status' in data:
        tarefa.status = data['status']
    else:
        tarefa.status = True

    db.session.commit()
    return jsonify({
        "mensagem": "Tarefa atulizada com sucesso",
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "status": tarefa.status
    })
