async function loadMsgs() {
    const res = await fetch('/api/messages');
    const msgs = await res.json();
    const el = document.getElementById('messages');
    el.innerHTML = '';
    if (msgs.length < 1) { el.textContent = 'No messages yet. ❤️'; return; }
    msgs.forEach((m, i) => {
        const article = document.createElement('article');
        article.innerHTML = `
            <h3>#${i+1} ${m.to ? '→ ' + m.to : ''}</h3>
            <p><strong>From:</strong> ${m.from}</p>
            <p class="message-text"></p>
            ${m.response ? '<p><strong>Response:</strong> ' + m.response + '</p>' : ''}
        `;
        el.appendChild(article);
        typeText(article.querySelector('.message-text'), m.message + ' ❤️');
    });
}

function typeText(el, text, speed = 50) {
    let i = 0;
    const timer = setInterval(() => {
        if (i < text.length) {
            el.innerHTML += text.charAt(i);
            i++;
        } else clearInterval(timer);
    }, speed);
}

function confettiBurst() {
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.top = '-10px';
        confetti.style.background = ['#ff69b4', '#ffb7c5', '#f472b6'][Math.floor(Math.random() * 3)];
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.borderRadius = '50%';
        confetti.style.opacity = '0.8';
        confetti.style.animation = 'fall 2s linear';
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 2000);
    }
}

const style = document.createElement('style');
style.innerHTML = '@keyframes fall { to { top: 100vh; transform: rotate(360deg); } }';
document.head.appendChild(style);

loadMsgs();

document.getElementById('msgForm').addEventListener('submit', async e => {
    e.preventDefault();
    const payload = {
        from: document.getElementById('from').value,
        to: document.getElementById('to').value,
        message: document.getElementById('message').value,
        response: document.getElementById('response').value
    };
    await fetch('/api/messages', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
    e.target.reset();
    await loadMsgs();
    confettiBurst();
});