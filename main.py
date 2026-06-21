import os 
import json
import customtkinter as ctk

ctk.set_appearance_mode('dark')
tarefas = []
if os.path.exists("tarefas.json"):
         with open("tarefas.json", "r", encoding="utf-8") as arquivo:
          tarefas = json.load(arquivo) 
    
def adicionar_tarefa():
    titulo = campo_titulo.get()
    descricao = campo_descricao.get()
    status = "pendente"
    tarefas.append({
        "titulo":titulo,
        "descrição":descricao,
        "status":status
    })
    with open("tarefas.json", "w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)
    
def listar_tarefas():
    for widget in box.winfo_children():
        widget.destroy()
    if not tarefas:
        label_mensagem= ctk.CTkLabel(box,text="Nenhuma tarefa encontrada ")
        label_mensagem.pack()
    else:
        label_mensagem= ctk.CTkLabel(box,text="\n---- Tarefas Encontrada ----")
        label_mensagem.pack()
        for tarefa in tarefas:
         label_mensagem = ctk.CTkLabel(box, text =f"Titulo: {tarefa['titulo']}".title())
         label_mensagem.pack()
         label_mensagem= ctk.CTkLabel(box, text=f"Descrição: {tarefa['descrição']}")
         label_mensagem.pack()
         label_mensagem= ctk.CTkLabel(box, text=f"Status: {tarefa['status']}".title())
         label_mensagem.pack()
         label_mensagem = ctk.CTkLabel(box,text="-" * 30)
         label_mensagem.pack()
              
def remover_tarefa():
    tarefa_remover = campo_titulo.get().strip().lower()
    tarefa_encontrada = False
    for tarefa in tarefas:
            if tarefa['titulo'].strip().lower() == tarefa_remover:
             tarefas.remove(tarefa)
             tarefa_encontrada = True
             break
           
    with open("tarefas.json", "w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)
    for widget in box.winfo_children():
        widget.destroy()
        
    if tarefa_encontrada:
        label_remover = ctk.CTkLabel(
         box,
         text='Tarefa removida com sucesso !!'
       )
        label_remover.pack()
        
    else:
        label_remover =ctk.CTkLabel(
            box,
            text='Terafa não encontrada'
        )
        label_remover.pack()
    listar_tarefas()
          
def editar_tarefa():
    tarefa_editar = campo_titulo.get().strip().lower()
    for tarefa in tarefas:
        if tarefa ['titulo'].strip().lower() == tarefa_editar:
           nova_descricao = campo_descricao.get()
           
           if nova_descricao:
               tarefa['descrição'] = nova_descricao
                
           with open("tarefas.json", "w", encoding="utf-8") as arquivo:
               json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)
                
           for widget in box.winfo_children():
                widget.destroy()    
           label_editar = ctk.CTkLabel(box, text='Tarefa editada com sucesso!')
           label_editar.pack()
           listar_tarefas()
           return
    for widget in box.winfo_children():
        widget.destroy()
    ctk.CTkLabel(box, text="Tarefa não encontrada.").pack()
    
def marcar_como_concluida():
    tarefa_concluida = campo_titulo.get()
    for tarefa in tarefas:
       if tarefa['titulo'] == tarefa_concluida:
            tarefa['status'] = "Concluida"
            
    with open("tarefas.json", "w", encoding="utf-8") as arquivo:
                json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)
              
# Criaçao da Janela Principal
app = ctk.CTk()
app.title('Sistema To-Do List')
app.geometry('300x300')


label_titulo= ctk.CTkLabel(app,text='Titulo')
label_titulo.pack(pady=5)

campo_titulo = ctk.CTkEntry(app,placeholder_text='Digite sua Tarefa')
campo_titulo.pack(pady=5)

label_descricao= ctk.CTkLabel(app,text='Descrição')
label_descricao.pack(pady=5)

campo_descricao = ctk.CTkEntry(app,placeholder_text="Descrição Tarefa")
campo_descricao.pack(pady=5)

botao = ctk.CTkButton(app,text='Adicionar', command= adicionar_tarefa)
botao.pack(pady=5)

botao_listar = ctk.CTkButton(app,text='Listar',command=listar_tarefas)
botao_listar.pack(pady=5)

botao_remover = ctk.CTkButton(app,text='Remover',command=remover_tarefa)
botao_remover.pack(pady=5)

botao_editar = ctk.CTkButton(app,text='Editar',command=editar_tarefa)
botao_editar.pack(pady=5)

botao_concluir = ctk.CTkButton(app,text='Concluir',command=marcar_como_concluida)
botao_concluir.pack(pady=5)
#List Box
box = ctk.CTkScrollableFrame(app,label_text="Lista de Tarefas")
box.pack(pady=5)
app.mainloop() 
