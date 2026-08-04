const API_BASE = '/api/tasks';

const listEl = document.getElementById('task-list');
const statusEl = document.getElementById('status-msg');
const addForm = document.getElementById('add-form');
const refreshBtn = document.getElementById('refresh-btn');

let tasks = [];

function showStatus(msg, isError=false){
  statusEl.textContent = msg;
  statusEl.classList.toggle('error', isError);
  if(msg){
    setTimeout(()=>{ if(statusEl.textContent === msg) statusEl.textContent = ''; }, 3500);
  }
}

function escapeHtml(str){
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// A API não expõe uma rota "listar todos", então descobrimos os ids
// varrendo sequencialmente até encontrar várias faltas seguidas.
async function fetchAllTasks(){
  const found = [];
  let consecutiveMisses = 0;
  let id = 1;
  const MAX_MISSES = 8;

  while(consecutiveMisses < MAX_MISSES){
    try{
      const res = await fetch(`${API_BASE}/${id}`);
      if(res.status === 404){
        consecutiveMisses++;
      } else if(res.ok){
        const data = await res.json();
        found.push(data);
        consecutiveMisses = 0;
      } else {
        consecutiveMisses++;
      }
    } catch(err){
      throw err;
    }
    id++;
  }
  return found;
}

function renderTasks(){
  if(tasks.length === 0){
    listEl.innerHTML = `<div class="empty">Nenhuma tarefa cadastrada ainda.</div>`;
    return;
  }

  listEl.innerHTML = tasks
    .slice()
    .sort((a,b) => a.id - b.id)
    .map(taskCardHtml)
    .join('');
}

function taskCardHtml(t){
  const idPad = String(t.id).padStart(3, '0');
  return `
  <div class="task-card ${t.status ? 'done' : ''}" data-id="${t.id}">
    <div class="task-top">
      <div>
        <div class="task-id">TAREFA #${idPad}</div>
        <h3 class="task-titulo">${escapeHtml(t.titulo)}</h3>
      </div>
      <div class="task-actions">
        <button class="icon-btn complete" title="${t.status ? 'Marcar como pendente' : 'Marcar como concluída'}" data-action="toggle">${t.status ? '↺' : '✓'}</button>
        <button class="icon-btn" title="Editar" data-action="edit">✎</button>
        <button class="icon-btn danger" title="Excluir" data-action="delete">✕</button>
      </div>
    </div>
    <p class="task-descricao">${escapeHtml(t.descricao)}</p>

    <div class="edit-fields">
      <div class="field">
        <label>Titulo</label>
        <input type="text" class="edit-titulo" maxlength="99" value="${escapeHtml(t.titulo)}">
      </div>
      <div class="field">
        <label>Descricao</label>
        <textarea class="edit-descricao" maxlength="99">${escapeHtml(t.descricao)}</textarea>
      </div>
      <div class="edit-actions">
        <button class="btn btn-ghost" data-action="cancel-edit" type="button">Cancelar</button>
        <button class="btn btn-primary" data-action="save-edit" type="button">Salvar</button>
      </div>
    </div>
  </div>`;
}

async function loadTasks(){
  showStatus('Carregando tarefas...');
  try{
    tasks = await fetchAllTasks();
    renderTasks();
    showStatus('');
  } catch(err){
    showStatus('Não foi possível carregar as tarefas.', true);
  }
}

addForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const titulo = document.getElementById('titulo').value.trim();
  const descricao = document.getElementById('descricao').value.trim();
  if(!titulo || !descricao) return;

  try{
    const res = await fetch(`${API_BASE}/add`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({titulo, descricao})
    });
    const data = await res.json();
    if(res.ok){
      addForm.reset();
      showStatus(data.mensagem || 'Tarefa adicionada.');
      await loadTasks();
    } else {
      showStatus(data.mensagem || 'Erro ao adicionar tarefa.', true);
    }
  } catch(err){
    showStatus('Erro de conexão com a API.', true);
  }
});

refreshBtn.addEventListener('click', loadTasks);

listEl.addEventListener('click', async (e) => {
  const btn = e.target.closest('button[data-action]');
  if(!btn) return;
  const card = btn.closest('.task-card');
  const id = card.dataset.id;
  const action = btn.dataset.action;

  if(action === 'delete'){
    if(!confirm('Excluir esta tarefa?')) return;
    try{
      const res = await fetch(`${API_BASE}/delete/${id}`, {method: 'DELETE'});
      const data = await res.json();
      showStatus(data.mensagem, !res.ok);
      if(res.ok){
        tasks = tasks.filter(t => t.id != id);
        renderTasks();
      }
    } catch(err){
      showStatus('Erro de conexão com a API.', true);
    }
  }

  if(action === 'toggle'){
    const t = tasks.find(t => t.id == id);
    try{
      const res = await fetch(`${API_BASE}/${id}/completed`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: !t.status})
      });
      const data = await res.json();
      if(res.ok){
        t.status = data.status;
        renderTasks();
        showStatus(data.mensagem);
      } else {
        showStatus(data.mensagem || 'Erro ao atualizar tarefa.', true);
      }
    } catch(err){
      showStatus('Erro de conexão com a API.', true);
    }
  }

  if(action === 'edit'){
    card.classList.add('editing');
  }

  if(action === 'cancel-edit'){
    card.classList.remove('editing');
  }

  if(action === 'save-edit'){
    const titulo = card.querySelector('.edit-titulo').value.trim();
    const descricao = card.querySelector('.edit-descricao').value.trim();
    if(!titulo || !descricao) return;
    try{
      const res = await fetch(`${API_BASE}/update/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({titulo, descricao})
      });
      const data = await res.json();
      if(res.ok){
        const t = tasks.find(t => t.id == id);
        t.titulo = titulo;
        t.descricao = descricao;
        card.classList.remove('editing');
        renderTasks();
        showStatus(data.mensagem);
      } else {
        showStatus(data.mensagem || 'Erro ao salvar.', true);
      }
    } catch(err){
      showStatus('Erro de conexão com a API.', true);
    }
  }
});

loadTasks();