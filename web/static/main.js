// Static Bharat Fashion AI — no build required
const fashionData = [{category:"Kurti",price:899,occasion:"Festival"},{category:"Jeans",price:999,occasion:"Casual"},{category:"Tshirt",price:599,occasion:"Casual"},{category:"Shirt",price:799,occasion:"Office"},{category:"Saree",price:1499,occasion:"Festival"},{category:"Jacket",price:1299,occasion:"Winter"},{category:"Dress",price:1199,occasion:"Party"}];
const myntraLinks = {Kurti:'https://www.myntra.com/kurti',Jeans:'https://www.myntra.com/jeans',Tshirt:'https://www.myntra.com/tshirts',Shirt:'https://www.myntra.com/shirts',Saree:'https://www.myntra.com/saree',Jacket:'https://www.myntra.com/jackets',Dress:'https://www.myntra.com/dresses'};

const app = document.getElementById('app');
const navbar = document.getElementById('navbar');
const footer = document.getElementById('footer');
const toTop = document.getElementById('toTop');

function renderNavbar(){
  navbar.innerHTML = `
    <div class="nav">
      <div style="display:flex;align-items:center;gap:16px">
        <div class="logo" onclick="navigate('home')">Bharat Fashion AI</div>
        <div class="nav-links">
          <button onclick="navigate('men')">Men</button>
          <button onclick="navigate('women')">Women</button>
          <button onclick="navigate('kids')">Kids</button>
          <button onclick="navigate('home')">Home & Living</button>
          <button onclick="navigate('beauty')">Beauty</button>
          <button onclick="navigate('categories')">Categories</button>
        </div>
      </div>
      <div class="nav-right">
        <input class="search" id="searchInput" placeholder="Search for products, brands and more" />
        <button class="toggle" id="darkToggle">Dark</button>
      </div>
    </div>`;
  document.getElementById('searchInput').addEventListener('keypress', (e)=>{if(e.key==='Enter') search(e.target.value)});
  document.getElementById('darkToggle').addEventListener('click', toggleDark);
}

function renderFooter(){
  footer.innerHTML = `<div class="footer">About Bharat Fashion AI • Privacy Policy • Terms & Conditions • Contact Us<br>© 2026 Bharat Fashion AI</div>`;
}

let dark = false;
function toggleDark(){dark = !dark; document.body.style.background = dark? '#111':'#F5F5F6'; document.body.style.color = dark? '#e7e7e7':'#282C3F';}

function navigate(page){location.hash = page;}
window.navigate = navigate;

function search(q){alert('Search: '+q)}

function renderHome(){
  app.innerHTML = `
  <div class="container">
    <section class="hero">
      <div class="hero-left">
        <h1>AI-Powered Bharat Fashion AI</h1>
        <p>Discover personalized fashion recommendations based on your occasion, budget and style preferences.</p>
        <div style="margin-top:12px">
          <button class="btn primary" onclick="navigate('categories')">Explore Categories</button>
          <a class="btn outline" href="https://www.myntra.com" target="_blank">Shop on Myntra</a>
        </div>
      </div>
      <div class="hero-right">
        <img src="https://images.unsplash.com/photo-1520975912507-7b4d6f5d6aef?auto=format&fit=crop&w=1000&q=80" alt="hero" />
      </div>
    </section>

    <section class="section">
      <h2>Trending Categories</h2>
      <div class="cards">` + fashionData.map(f=>`
        <div class="cat-card">
          <img src="https://source.unsplash.com/400x400/?${f.category}" alt="${f.category}" />
          <div class="cat-body">
            <div class="cat-title">${f.category}</div>
            <div class="cat-meta">Starting ₹${f.price} • <span class="tag">${f.occasion}</span></div>
          </div>
        </div>`).join('') + `
      </div>
    </section>

    <section class="section offers">
      <h2>Featured Offers</h2>
      <div class="offer-grid">
        <div class="offer">Festival Collection</div>
        <div class="offer">Casual Collection</div>
        <div class="offer">Office Wear</div>
        <div class="offer">Winter Collection</div>
        <div class="offer">Party Collection</div>
      </div>
    </section>

    <section class="section why">
      <h2>Why Bharat Fashion AI?</h2>
      <div class="why-grid">
        <div class="why-card">🤖<div>AI Recommendations</div></div>
        <div class="why-card">💸<div>Budget Friendly</div></div>
        <div class="why-card">🎯<div>Occasion Based</div></div>
        <div class="why-card">🔗<div>Direct Myntra Shopping</div></div>
      </div>
    </section>

  </div>`;
}

function renderCategories(){
  let occasion = 'Festival';
  let budget = 1000;
  function build(){
    const filtered = fashionData.filter(f=> f.price<=budget && (occasion? f.occasion===occasion : true));
    document.getElementById('app').innerHTML = `
      <div class="container">
        <h2>Recommendations</h2>
        <div class="filters">
          <label>Occasion
            <select id="occSelect">
              <option>Festival</option>
              <option>Casual</option>
              <option>Office</option>
              <option>Winter</option>
              <option>Party</option>
            </select>
          </label>
          <label>Budget ₹<span id="budVal">${budget}</span>
            <input id="budRange" type="range" min="500" max="2000" value="${budget}" />
          </label>
        </div>
        <div class="rec-grid">` + filtered.map(item=>{
          const score = scoreMatch(item, occasion, budget);
          const link = myntraLinks[item.category] || `https://www.myntra.com/search/${encodeURIComponent(item.category)}`;
          return `
          <div class="rec-card">
            <img src="https://source.unsplash.com/400x400/?${item.category}" alt="${item.category}" />
            <div class="rec-body">
              <div class="rec-title">${item.category}</div>
              <div class="rec-meta">₹${item.price} • <span class="tag">${item.occasion}</span></div>
              <div class="score">${score}% Match</div>
              <a class="btn primary" href="${link}" target="_blank">Shop on Myntra</a>
            </div>
          </div>`}).join('') + `</div>
      </div>`;
    document.getElementById('occSelect').value = occasion;
    document.getElementById('occSelect').addEventListener('change',(e)=>{occasion=e.target.value;build();});
    document.getElementById('budRange').addEventListener('input',(e)=>{budget=Number(e.target.value);document.getElementById('budVal').innerText=budget;build();});
  }
  build();
}

function scoreMatch(item, occasion, budget){
  let score = 50;
  if(item.occasion.toLowerCase() === occasion.toLowerCase()) score += 40;
  const diff = Math.abs(item.price - budget);
  score += Math.max(0, 30 - Math.round(diff/50));
  return Math.min(100, score);
}

function renderAI(){
  document.getElementById('app').innerHTML = `
    <div class="container">
      <h2>AI Assistant</h2>
      <div class="chatbox">
        <div class="messages" id="messages"></div>
        <div class="chat-input">
          <input id="chatInput" placeholder='Try: "Festival wear under ₹1000"' />
          <button class="btn primary" id="askBtn">Ask</button>
        </div>
      </div>
    </div>`;
  document.getElementById('askBtn').addEventListener('click', ()=>{
    const q = document.getElementById('chatInput').value.trim(); if(!q) return;
    addMessage('user', q);
    const matches = findMatches(q);
    const botText = matches.slice(0,3).map(m=>`${m.item.category} ₹${m.item.price} — ${m.score}% Match`).join('\n');
    addMessage('bot', botText);
    const messagesEl = document.getElementById('messages');
    matches.slice(0,3).forEach(m=>{
      const div = document.createElement('div'); div.className='match';
      div.innerHTML = `<img src="https://source.unsplash.com/120x120/?${m.item.category}" alt=""><div><div class="rec-title">${m.item.category}</div><div class="price">₹${m.item.price}</div><a class="btn" href="${m.link}" target="_blank">Shop on Myntra</a></div>`;
      messagesEl.appendChild(div);
    });
    document.getElementById('chatInput').value='';
  });
}

function addMessage(who, text){
  const messagesEl = document.getElementById('messages') || document.createElement('div');
  if(!messagesEl.id) messagesEl.id='messages';
  const div = document.createElement('div'); div.className='msg '+(who==='user'?'user':'bot');
  div.innerHTML = `<pre style="white-space:pre-wrap">${text}</pre>`;
  messagesEl.appendChild(div);
  if(document.getElementById('messages')) document.getElementById('messages').scrollTop = messagesEl.scrollHeight;
}

function findMatches(query){
  const q = query.toLowerCase();
  const results = [];
  fashionData.forEach(item=>{
    if(q.includes(item.occasion.toLowerCase()) || q.includes(item.category.toLowerCase())){
      let score = 90;
      if(q.includes('under')){
        const m = q.match(/\d+/);
        if(m){const num=Number(m[0]); if(item.price>num) score-=40}
      }
      results.push({item,score,link:myntraLinks[item.category]});
    }
  });
  if(results.length===0){
    fashionData.filter(f=>f.occasion==='Casual').forEach(c=>results.push({item:c,score:80,link:myntraLinks[c.category]}));
  }
  return results;
}

// Router
function router(){
  const hash = location.hash.replace('#','') || 'home';
  renderNavbar(); renderFooter();
  if(hash==='home') renderHome();
  else if(hash==='categories') renderCategories();
  else if(hash==='ai') renderAI();
  else renderHome();
}

window.addEventListener('hashchange', router);
window.addEventListener('load', ()=>{ if(!location.hash) location.hash='home'; router(); });

toTop.addEventListener('click', ()=>window.scrollTo({top:0,behavior:'smooth'}));

