import React, {useState} from 'react';
import { fashionData, myntraLinks } from '../data/fashionData';

function findMatches(query){
  const q = query.toLowerCase();
  const results = [];
  fashionData.forEach(item=>{
    if(q.includes(item.occasion.toLowerCase()) || q.includes(item.category.toLowerCase())){
      // estimate score
      let score = 90;
      if(q.includes('under')){
        const m = q.match(/\d+/);
        if(m){
          const num = Number(m[0]);
          if(item.price > num) score -= 40;
        }
      }
      results.push({item, score, link: myntraLinks[item.category]});
    }
  });
  if(results.length===0){
    // fallback: casual picks
    const casual = fashionData.filter(f=>f.occasion==='Casual');
    casual.forEach(c=>results.push({item:c,score:80,link:myntraLinks[c.category]}));
  }
  return results;
}

export default function Chatbot(){
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  function send(){
    if(!input) return;
    const user = {from:'user', text:input};
    const matches = findMatches(input);
    const botText = matches.slice(0,3).map(m=>`${m.item.category} ₹${m.item.price} — ${m.score}% Match`).join('\n');
    const bot = {from:'bot', text:botText, matches};
    setMessages(prev=>[...prev, user, bot]);
    setInput('');
  }

  return (
    <main className="container">
      <h2>AI Assistant</h2>
      <div className="chatbox">
        <div className="messages">
          {messages.map((m,i)=> (
            <div key={i} className={`msg ${m.from}`}><pre>{m.text}</pre>{m.matches && m.matches.map((mm,idx)=> (
              <div className="match" key={idx}>
                <img src={`https://source.unsplash.com/120x120/?${mm.item.category}`} alt="pic" />
                <div>
                  <div className="rec-title">{mm.item.category}</div>
                  <div className="price">₹{mm.item.price}</div>
                  <a className="btn" href={mm.link} target="_blank" rel="noreferrer">Shop on Myntra</a>
                </div>
              </div>
            ))}</div>
          ))}
        </div>
        <div className="chat-input">
          <input value={input} onChange={e=>setInput(e.target.value)} placeholder='Try: "Festival wear under ₹1000"' />
          <button className="btn primary" onClick={send}>Ask</button>
        </div>
      </div>
    </main>
  )
}
