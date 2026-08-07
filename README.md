# Gerenciador de Tarefas

Aplicação web para gerenciamento de tarefas (to-do list), construída com **Flask** no back-end e **HTML, CSS e JavaScript puro** no front-end, com autenticação de usuário via **Flask-Login**.

## Funcionalidades

- Cadastro de usuário
- Login e logout com sessão
- Adicionar tarefa (título e descrição)
- Listar tarefas
- Editar título/descrição de uma tarefa
- Marcar tarefa como concluída ou pendente
- Excluir tarefa

## Tecnologias utilizadas

- [Flask](https://flask.palletsprojects.com/) — framework web em Python
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM para o banco de dados
- [Flask-Login](https://flask-login.readthedocs.io/) — gerenciamento de sessão e autenticação
- SQLite — banco de dados
- HTML, CSS e JavaScript (Vanilla) — interface do usuário

## Estrutura do projeto

```
daily_list_system/
├── app.py
├── tarefa.db
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Como executar o projeto

### 1. Pré-requisitos

- Python 3 instalado

### 2. Instalar as dependências

```bash
pip install flask flask-sqlalchemy flask-login
```

### 3. Rodar a aplicação

```bash
python app.py
```

O banco de dados (`tarefa.db`) é criado automaticamente na primeira execução.

### 4. Acessar

Abra o navegador em:

```
http://127.0.0.1:5000
```

## Rotas da API

### Usuário

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/register` | Cadastra um novo usuário |
| POST | `/api/login` | Autentica o usuário e inicia a sessão |
| POST | `/api/logout` | Encerra a sessão do usuário |

### Tarefas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/tasks/add` | Adiciona uma nova tarefa |
| GET | `/api/tasks/<id>` | Retorna os dados de uma tarefa específica |
| PUT | `/api/tasks/update/<id>` | Atualiza título, descrição e/ou status de uma tarefa |
| PATCH | `/api/tasks/<id>/completed` | Marca uma tarefa como concluída ou pendente |
| DELETE | `/api/tasks/delete/<id>` | Remove uma tarefa |

Todas as rotas de tarefas exigem que o usuário esteja autenticado.

### Exemplo de requisição

**Adicionar tarefa**
```json
POST /api/tasks/add
{
  "titulo": "Estudar Flask",
  "descricao": "Revisar rotas e templates"
}
```

**Resposta**
```json
{
  "mensagem": "Tarefa adicionada com sucesso"
}
```

## Como funciona o front-end

O `script.js` se comunica com as rotas do `app.py` usando `fetch()`. Cada ação do usuário na interface (adicionar, editar, concluir ou excluir tarefa) dispara uma requisição HTTP para a rota correspondente da API, que responde em formato JSON e atualiza a tela.

