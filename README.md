# ✅ Sistema To-Do List — Gerenciador de Tarefas Desktop

Aplicação **desktop** simples para gerenciamento de tarefas (To-Do List), desenvolvida em **Python** com interface gráfica feita em **CustomTkinter** e persistência de dados em arquivo **JSON**.

> Projeto com fins de estudo, focado em prática de interface gráfica (GUI) e manipulação de arquivos em Python.

---

## 🗂️ Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Funciona](#-como-funciona)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Executando o Projeto](#-executando-o-projeto)

---

## 🔎 Visão Geral

O **Sistema To-Do List** é uma janela desktop onde o usuário pode cadastrar tarefas com título e descrição, listá-las, editá-las, marcá-las como concluídas e removê-las. Não depende de internet, banco de dados externo ou servidor — tudo roda localmente e os dados são salvos em um arquivo `tarefas.json` na própria pasta do projeto.

---

## ✨ Funcionalidades

| Botão | Ação |
|---|---|
| **Adicionar** | Cria uma nova tarefa com o título e a descrição digitados, status inicial `"pendente"`. |
| **Listar** | Exibe na tela todas as tarefas cadastradas, com título, descrição e status. |
| **Remover** | Remove a tarefa cujo título corresponde ao texto digitado no campo "Título". |
| **Editar** | Localiza uma tarefa pelo título e atualiza título/descrição com os novos valores digitados. |
| **Concluir** | Marca a tarefa correspondente ao título digitado com status `"Concluida"`. |

Todas as alterações (adicionar, remover, editar, concluir) são gravadas automaticamente no arquivo `tarefas.json`.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — biblioteca para interface gráfica moderna (baseada no Tkinter)
- **JSON** — formato usado para persistir as tarefas em disco
- **os** — módulo padrão do Python usado para verificar a existência do arquivo de dados

---

## 📁 Estrutura do Projeto

```
Task_management_system-main/
│
├── main.py          # Código principal: interface gráfica e lógica das tarefas
├── tarefas.json      # Arquivo de persistência (lista de tarefas em JSON)
└── README.md
```

---

## ⚙️ Como Funciona

- As tarefas são armazenadas em memória como uma **lista de dicionários**, e cada tarefa possui três campos:
  - `titulo`
  - `descrição`
  - `status` (`"pendente"` ou `"Concluida"`)
- Ao iniciar, o programa verifica se já existe um `tarefas.json` e, se sim, carrega as tarefas salvas anteriormente.
- A cada operação (adicionar, remover, editar, concluir), a lista completa é regravada no `tarefas.json`, garantindo que os dados persistam mesmo após fechar o programa.
- A busca por tarefas (para remover, editar ou concluir) é feita comparando o texto digitado no campo **Título** com o título já cadastrado.

> ⚠️ **Atenção:** atualmente a busca usada em `remover_tarefa` compara o título já em minúsculo/sem espaços (`.strip().lower()`) com o título original salvo (sem essa normalização) em `editar_tarefa` e `marcar_como_concluida` — ou seja, **remover** tende a funcionar de forma case-insensitive, enquanto **editar** e **concluir** exigem que o título digitado seja **idêntico** (incluindo maiúsculas/minúsculas) ao que está salvo.

---

## ⚙️ Instalação e Configuração

### 1. Clone ou extraia o projeto

```bash
git clone <url-do-repositorio>
cd Task_management_system-main
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install customtkinter
```

---

## ▶️ Executando o Projeto

```bash
python main.py
```

Uma janela de **300x300** será aberta com os campos de título e descrição, os botões de ação e a lista de tarefas.

---


