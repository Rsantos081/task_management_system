from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefa.db'
db = SQLAlchemy(app)

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(99), nullable=False)
    descricao = db.Column(db.String(99), nullable=False)
    status = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks/add', methods = ['POST'])
def add_tasks():
    data = request.json
    if 'titulo' in data and 'descricao' in data:
        tasks = Tarefas(titulo=data["titulo"],descricao=data["descricao"])
        db.session.add(tasks)
        db.session.commit()
        return jsonify ({"mensagem":"Tarefa adicionada com sucesso"})
    return jsonify ({"mensagem":"Dados invalido da Tarefa"}), 400

@app.route('/api/tasks/delete/<int:id>', methods = ['DELETE'])
def remove_tasks(id):
    id = Tarefas.query.get(id)
    if id:
        db.session.delete(id)
        db.session.commit()
        return jsonify ({"mensagem":"Tarefa removida com sucesso"})
    return jsonify ({"mensagem":"Tarefa não encontrada Id invalido"}), 400

@app.route('/api/tasks/<int:id>', methods = ['GET'])
def list_tasks(id):
    id = Tarefas.query.get(id)
    if id:
        return jsonify({
            "id":id.id,
            "titulo":id.titulo,
            "descricao":id.descricao,
            "status":id.status
        })
    return jsonify({"mensagem":"Tarefa não enontrado"}), 404

@app.route('/api/tasks/update/<int:id>', methods = ['PUT'])
def update_tasks(id):
    id = Tarefas.query.get(id)
    if not id:
        return jsonify ({"mensagem":"Tarefa não encontrada"}), 404
    data = request.json
    
    if 'titulo' in data:
        id.titulo = data['titulo']
        
    if 'descricao' in data:
        id.descricao = data['descricao']
        
    if 'status' in data:
        id.status = data['status']
    db.session.commit()
    return jsonify({"mensagem":"Tarefa atualizada com sucesso"})
        
@app.route('/api/tasks/<int:id>/completed', methods = ['PATCH'])
def mark_task_completed(id):
    tarefa = Tarefas.query.get(id)
    if not tarefa:
        return jsonify ({"mensagem":"Tarefa não encontrada"}), 404
    data = request.json
    
    if 'status' in data:
        tarefa.status = data['status']
    else:
        tarefa.status = True
    
    db.session.commit()
    return jsonify({
        "mensagem":"Tarefa atulizada com sucesso",
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "status": tarefa.status        
    })
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
