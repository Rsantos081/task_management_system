from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefa.db'
app.config ['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = "login"



class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    tarefas = db.relationship('Tarefas', backref='usuario', lazy=True)
    
class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(99), nullable=False)
    descricao = db.Column(db.String(99), nullable=False)
    status = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    
@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))
   
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/login', methods = ['POST'])
def login():
    data = request.json
    user = Usuario.query.filter_by(nome=data.get("nome")).first()
    
    if user and data.get("senha") == user.senha:
        login_user(user)
        return jsonify ({"mensagem": "Usuario Autenticado com Sucesso"})
    
    return jsonify ({"mensagem": "Credencias Invalidas do Usuario"}), 401   

@app.route('/api/logout', methods = ['POST'])
def logout():
    logout_user()
    return jsonify ({"mensagem": "Logout Realizado com Sucesso"})

@app.route('/api/register/', methods = ['POST'])
def register():
    data = request.json
    if 'nome' in data and 'senha' in data:
        if Usuario.query.filter_by(nome=data["nome"]).first():
            return jsonify ({"mensagem":"Usuario ja existe"}), 400
        usuario = Usuario(nome=data["nome"], senha=data["senha"])
        db.session.add(usuario)
        db.session.commit()
        return jsonify ({"mensagem":"Usuario Cadastrado com Sucesso"}), 200
    return jsonify ({"mensagem":"Dados Invalidos do Usuario"}), 400

@app.route('/api/tasks', methods=['GET'])
@login_required
def  list_all_tasks():
    tarefas = Tarefas.query.filter_by(usuario_id=current_user.id).all()
    return jsonify([
        {
        "id": t.id,
        "titulo": t.titulo,
        "descricao":t.descricao,
        "status": t.status
       } for t in tarefas    
    ]) 
          
@app.route('/api/tasks/add', methods = ['POST'])
@login_required
def add_tasks():
    data = request.json
    if 'titulo' in data and 'descricao' in data:
        tasks = Tarefas(
            titulo=data["titulo"],
            descricao=data["descricao"],
            usuario_id = current_user.id    
        )
        db.session.add(tasks)
        db.session.commit()
        return jsonify ({"mensagem":"Tarefa adicionada com sucesso"})
    return jsonify ({"mensagem":"Dados invalido da Tarefa"}), 400

@app.route('/api/tasks/delete/<int:id>', methods = ['DELETE'])
@login_required  
def remove_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id = current_user.id).first()
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
        return jsonify ({"mensagem":"Tarefa removida com sucesso"})
    return jsonify ({"mensagem":"Tarefa não encontrada Id invalido"}), 400

@app.route('/api/tasks/<int:id>', methods = ['GET'])
@login_required
def list_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id,usuario_id=current_user.id).first()
    if tarefa:
        return jsonify({
            "id":tarefa.id,
            "titulo":tarefa.titulo,
            "descricao":tarefa.descricao,
            "status":tarefa.status
        })
    return jsonify({"mensagem":"Tarefa não enontrado"}), 404

@app.route('/api/tasks/update/<int:id>', methods = ['PUT'])
@login_required
def update_tasks(id):
    tarefa = Tarefas.query.filter_by(id=id, usuario_id = current_user.id).first()
    if not tarefa:
        return jsonify ({"mensagem":"Tarefa não encontrada"}), 404
    data = request.json
    
    if 'titulo' in data:
        tarefa.titulo = data['titulo']
        
    if 'descricao' in data:
        tarefa.descricao = data['descricao']
        
    if 'status' in data:
        tarefa.status = data['status']
    db.session.commit()
    return jsonify({"mensagem":"Tarefa atualizada com sucesso"})
        
@app.route('/api/tasks/<int:id>/completed', methods = ['PATCH'])
@login_required
def mark_task_completed(id):
    tarefa = Tarefas.query.filter_by(id=id,usuario_id=current_user.id).first()
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
