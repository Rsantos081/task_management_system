# Gerenciamento de Tarefas

Sistema de gerenciamento de tarefas (to-do list) com autenticação de usuários, feito em **Flask** + **SQLAlchemy** + **Flask-Login**. Cada usuário só visualiza e gerencia as próprias tarefas.

## Tecnologias

- Python 3
- Flask
- Flask-SQLAlchemy (ORM)
- Flask-Login (autenticação e sessão de usuário)
- SQLite (banco de dados)
- JavaScript, HTML e CSS (Interface do Usuario)

## Funcionalidades

- Cadastro de usuário
- Login e logout com sessão
- Criação, listagem, atualização e remoção de tarefas
- Marcar tarefa como concluída
- Tarefas isoladas por usuário (cada usuário só acessa as suas)

## Estrutura do banco de dados

**Usuario**
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária |
| nome | String(255) | Nome de usuário (único) |
| senha | String(100) | Senha do usuário |

**Tarefas**
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária |
| titulo | String(99) | Título da tarefa |
| descricao | String(99) | Descrição da tarefa |
| status | Boolean | Se a tarefa está concluída |
| usuario_id | Integer (FK) | Usuário dono da tarefa |

## Estrutura de pastas

```
Task_management_system/
│
├── app.py                 # Aplicação principal: models, rotas e configuração do Flask
├── instance/
│   └── tarefa.db           # Banco de dados SQLite (gerado automaticamente na 1ª execução)
├── static/
│   ├── script.js            # JavaScript do front-end
│   └── style.css            # Estilos do front-end
├── templates/
│   └── index.html           # Página inicial renderizada pela rota "/"
├── .gitignore
└── README.md
```

> **Sobre a pasta `instance/`:** como a `SQLALCHEMY_DATABASE_URI` está configurada como `sqlite:///tarefa.db` (caminho relativo), o Flask cria o banco automaticamente dentro de uma pasta especial chamada `instance/`, e não na raiz do projeto. Isso é um comportamento padrão do Flask para separar arquivos "de instância" (configs locais, banco de dados) do código-fonte versionado. Por isso, se for apagar o banco para recriar o schema, o comando correto é:
> ```powershell
> Remove-Item .\instance\tarefa.db
> ```

## Instalação

### 1. Clone o repositório e entre na pasta do projeto

```bash
git clone <url-do-repositorio>
cd daily_list_system
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
```

Ativar no Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Ativar no Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install flask flask-sqlalchemy flask-login
```

### 4. Configure a variável de ambiente `SECRET_KEY`

No PowerShell:
```powershell
$env:SECRET_KEY = "uma-chave-secreta-qualquer"
```

No Linux/Mac:
```bash
export SECRET_KEY="uma-chave-secreta-qualquer"
```

### 5. Rode o projeto

```bash
python app.py
```

O banco `tarefa.db` é criado automaticamente na primeira execução. A aplicação sobe em `http://127.0.0.1:5000`.

> ⚠️ Se você alterar a estrutura de alguma tabela (adicionar/remover coluna) depois que o banco já existir, `db.create_all()` **não atualiza** tabelas já existentes. Apague o `tarefa.db` e rode `python app.py` de novo para recriá-lo do zero (isso apaga os dados).

## Endpoints da API

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/register/` | Cadastra um novo usuário |
| POST | `/api/login` | Autentica o usuário e inicia a sessão |
| POST | `/api/logout` | Encerra a sessão do usuário |

**Exemplo de body — registro/login:**
```json
{
  "nome": "ruant",
  "senha": "123456"
}
```

### Tarefas
*(todas exigem estar logado — envie o cookie de sessão obtido no login)*

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/tasks` | Lista todas as tarefas do usuário logado |
| GET | `/api/tasks/<id>` | Detalha uma tarefa específica |
| POST | `/api/tasks/add` | Cria uma nova tarefa |
| PUT | `/api/tasks/update/<id>` | Atualiza título, descrição e/ou status |
| PATCH | `/api/tasks/<id>/completed` | Marca a tarefa como concluída |
| DELETE | `/api/tasks/delete/<id>` | Remove uma tarefa |

**Exemplo de body — criar tarefa:**
```json
{
  "titulo": "Deploy",
  "descricao": "Toda Segunda-Feira"
}
```

## Segurança e isolamento por usuário

Toda tarefa é vinculada ao usuário que a criou através da coluna `usuario_id`. As rotas usam `current_user` (fornecido pelo Flask-Login) para filtrar as consultas, garantindo que um usuário não visualize, edite ou apague tarefas de outro usuário.
