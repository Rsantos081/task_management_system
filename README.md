## Sistema To-Do List com Python + CustomTkinter
Este projeto é uma aplicação desktop simples de gerenciamento de tarefas (To-Do List), desenvolvida em Python utilizando a biblioteca CustomTkinter para interface gráfica moderna e JSON para persistência de dados.

# Funcionalidades
- Adicionar novas tarefas
- Listar tarefas cadastradas
- Editar tarefas existentes
- Remover tarefas
- Marcar tarefas como concluídas
- Salvamento automático em arquivo tarefas.json

# Tecnologias utilizadas
- Python 3
- CustomTkinter (interface gráfica)
- JSON (armazenamento de dados)
- OS (manipulação de arquivos)

# Projeto
 - tarefas.json      # Banco de dados local
 - app.py            # Código principal da aplicação
   
# Como Executar
1. Clone Repositorio = https://github.com/Rsantos081/To-Do-List
2. cd To-Do-List.git
3. python install customtkinter
4. python app.py

# Como funciona
- As tarefas são armazenadas em uma lista de dicionários.
- Cada tarefa possui:
 Titulo
 Descrição
 Status (pendente ou concluída)
- Os dados são salvos automaticamente no arquivo tarefas.json, garantindo persistência mesmo após  fechar o programa.

