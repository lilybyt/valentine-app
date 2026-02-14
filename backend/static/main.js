async function loadMsgs(){
  const res = await fetch('/api/messages');
  const msgs = await res.json();
  const el = document.getElementById('messages');
  if(!msgs.length){ el.textContent = 'No messages yet.'; return; }
  el.innerHTML = msgs.map((m,i)=>`<article><h3>💌 #${i+1} ${m.to ? '→ '+m.to : ''}</h3><p><strong>From:</strong> ${m.from}</p><p>${m.message}</p><p><em>${m.response||''}</em></p></article>`).join('');
}
document.getElementById('msgForm').addEventListener('submit', async e=>{
  e.preventDefault();
  const payload = {
    from: document.getElementById('from').value,
    to: document.getElementById('to').value,
    message: document.getElementById('message').value,
    response: document.getElementById('response').value
  };
  await fetch('/api/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  e.target.reset();
  await loadMsgs();
});
loadMsgs();