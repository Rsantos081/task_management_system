# Gerenciador de Tarefas

Aplicação web para gerenciamento de tarefas (to-do list), construída com **Flask** no back-end e **HTML, CSS e JavaScript puro** no front-end, com autenticação de usuário via **Flask-Login**.

Organizada com **Flask Blueprints**: cada domínio (autenticação e tarefas) vive em seu próprio módulo, registrado por uma application factory (`create_app`).

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
task_management_system/
├── run.py # ponto de entrada: cria a app e roda
├── requirements.txt
├── app/
│ ├── init.py # application factory (create_app), registra os blueprints
│ ├── extensions.py # instâncias soltas: db, login_manager
│ ├── models.py # models Usuario e Tarefas
│ │
│ ├── auth/ # domínio: autenticação
│ │ ├── init.py # auth_bp = Blueprint("auth", name, url_prefix="/api")
│ │ └── routes.py # /api/login, /api/register, /api/logout
│ │
│ ├── main/ # domínio: página inicial
│ │ ├── init.py # main_bp = Blueprint("main", name)
│ │ └── routes.py # /
│ │
│ └── tasks/ # domínio: tarefas
│ ├── init.py # tasks_bp = Blueprint("tasks", name, url_prefix="/api/tasks")
│ └── routes.py # /, /add, /<id>, /update/<id>, /delete/<id>, /<id>/completed
│
├── templates/
│ └── index.html
├── static/
│ ├── style.css
│ └── script.js
└── instance/
└── tarefa.db # criado automaticamente na primeira execução`
```
## Como executar o projeto

### 1. Pré-requisitos

- Python 3 instalado

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Definir a variável de ambiente SECRET_KEY

```bash
export SECRET_KEY="troque-por-uma-chave-secreta"   # Linux/macOS
set SECRET_KEY=troque-por-uma-chave-secreta         # Windows (cmd)
```

### 4. Rodar a aplicação

```bash
python run.py
```

O banco de dados (`instance/tarefa.db`) é criado automaticamente na primeira execução.

### 5. Acessar

Abra o navegador em: http://127.0.0.1:5000

## Rotas da API

### Usuário (`auth_bp`, prefixo `/api`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/register` | Cadastra um novo usuário |
| POST | `/api/login` | Autentica o usuário e inicia a sessão |
| POST | `/api/logout` | Encerra a sessão do usuário |

### Página (`main_bp`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Renderiza a página principal (index.html) |

### Tarefas (`tasks_bp`, prefixo `/api/tasks`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/tasks/` | Lista as tarefas do usuário logado |
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
O `script.js` se comunica com as rotas registradas pelos blueprints usando `fetch()`. Cada ação do usuário na interface (adicionar, editar, concluir ou excluir tarefa) dispara uma requisição HTTP para a rota correspondente da API, que responde em formato JSON e atualiza a tela.
