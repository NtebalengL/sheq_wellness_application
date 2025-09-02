// Theme toggle and persistence
const themeToggleButtons = document.querySelectorAll('[id^=themeToggle]');
function setTheme(isDark){
  document.body.classList.toggle('dark-mode', isDark);
  localStorage.setItem('sheq_dark', isDark ? '1' : '0');
}
function initTheme(){
  const stored = localStorage.getItem('sheq_dark');
  const dark = stored === '1' || (stored === null && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  setTheme(dark);
}
initTheme();

document.addEventListener('click', (e)=>{
  if(e.target && e.target.id && e.target.id.startsWith('themeToggle')){
    setTheme(!document.body.classList.contains('dark-mode'));
  }
});

// -- Auth (login/register)
const loginForm = document.getElementById('loginForm');
if(loginForm){
  loginForm.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    try{
      const res = await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});
      const data = await res.json();
      document.getElementById('authMsg').innerText = data.message || (data.success ? 'Logged in' : 'Login failed');
      if(data.success) location.href = 'index.html';
    }catch(e){ document.getElementById('authMsg').innerText = 'Network error'; }
  });
}

const regForm = document.getElementById('registerForm');
if(regForm){
  regForm.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    try{
      const res = await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,email,password})});
      const data = await res.json();
      document.getElementById('authMsg').innerText = data.message || 'Registered';
    }catch(e){document.getElementById('authMsg').innerText='Network error';}
  });
}

// -- Report form
const reportForm = document.getElementById('reportForm');
if(reportForm){
  reportForm.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const type = document.getElementById('r_type').value;
    const message = document.getElementById('r_message').value;
    const contact = document.getElementById('r_contact').value || null;
    const payload = { user_id: null, report_type: type, message: message, contact };
    try{
      const res = await fetch('/api/report',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      const data = await res.json();
      document.getElementById('reportMsg').innerText = data.message || 'Report submitted';
      reportForm.reset();
    }catch(e){document.getElementById('reportMsg').innerText='Network error submitting report';}
  });
}

// -- Chat bot
const chatForm = document.getElementById('chatForm');
if(chatForm){
  const chatLog = document.getElementById('chatLog');
  chatForm.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const txt = document.getElementById('chatInput').value.trim();
    if(!txt) return;
    appendMessage('You', txt);
    document.getElementById('chatInput').value = '';
    appendMessage('Bot', 'Searching...');
    try{
      const res = await fetch('/api/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
      const data = await res.json();
      // replace last bot message
      const nodes = chatLog.querySelectorAll('.chat-entry');
      if(nodes.length){ nodes[nodes.length-1].querySelector('.entry-text').innerText = data.answer || 'No response'; }
    }catch(e){ appendMessage('Bot','Network error'); }
  });
}
function appendMessage(who, text){
  const chatLog = document.getElementById('chatLog');
  const wrap = document.createElement('div'); wrap.className='chat-entry';
  wrap.innerHTML = `<strong class="muted">${who}:</strong> <div class="entry-text">${escapeHtml(text)}</div>`;
  chatLog.appendChild(wrap);
  chatLog.scrollTop = chatLog.scrollHeight;
}
function escapeHtml(s){ return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }

// -- Admin fetch (note: protect endpoints server-side)
if(document.getElementById('adminUsers')){
  (async function(){
    try{
      const ures = await fetch('/api/admin/users');
      const users = await ures.json();
      const tbodyU = document.querySelector('#adminUsers tbody');
      users.forEach(u=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${u.id}</td><td>${u.name}</td><td>${u.email}</td><td>${u.created_at}</td>`; tbodyU.appendChild(tr);});

      const rres = await fetch('/api/admin/reports');
      const reports = await rres.json();
      const tbodyR = document.querySelector('#adminReports tbody');
      reports.forEach(r=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.id}</td><td>${r.user_id||''}</td><td>${r.report_type}</td><td>${r.message}</td><td>${r.created_at}</td>`; tbodyR.appendChild(tr);});
    }catch(e){ console.warn('admin fetch failed', e); }
  })();
}

// initialize toggles if any created dynamically
window.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('[id^=themeToggle]').forEach(b=>b.addEventListener('click', ()=> setTheme(!document.body.classList.contains('dark-mode'))));
});
