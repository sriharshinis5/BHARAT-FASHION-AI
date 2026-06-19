import React, {useState} from 'react';
import { fashionData, myntraLinks } from '../data/fashionData';

function scoreMatch(item, occasion, budget){
  let score = 50;
  if(item.occasion.toLowerCase() === occasion.toLowerCase()) score += 40;
  // price closeness
  const diff = Math.abs(item.price - budget);
  score += Math.max(0, 30 - Math.round(diff/50));
  return Math.min(100, score);
}

export default function Recommendations(){
  const [occasion, setOccasion] = useState('Festival');
  const [budget, setBudget] = useState(1000);

  const filtered = fashionData.filter(f => f.price <= budget && (occasion? f.occasion===occasion : true));

  return (
    <main className="container">
      <h2>Recommendations</h2>
      <div className="filters">
        <label>Occasion
          <select value={occasion} onChange={e=>setOccasion(e.target.value)}>
            <option>Festival</option>
            <option>Casual</option>
            <option>Office</option>
            <option>Winter</option>
            <option>Party</option>
          </select>
        </label>
        <label>Budget ₹{budget}
          <input type="range" min="500" max="2000" value={budget} onChange={e=>setBudget(Number(e.target.value))} />
        </label>
      </div>

      <div className="rec-grid">
        {filtered.length===0 && <div className="muted">No items match your filters.</div>}
        {filtered.map(item=>{
          const score = scoreMatch(item, occasion, budget);
          const link = myntraLinks[item.category] || `https://www.myntra.com/search/${encodeURIComponent(item.category)}`;
          return (
            <div key={item.category} className="rec-card">
              <img
                src={(() => {
                  const categoryToImage = {
                    Kurti: '/assets/kurti.svg',
                    Jeans: '/assets/jeans.svg',
                    Tshirt: '/assets/tshirt.svg',
                    Shirt: '/assets/shirt.svg',
                    Saree: '/assets/saree.svg',
                    Jacket: '/assets/jacket.svg',
                    Dress: '/assets/dress.svg',
                  };
                  return categoryToImage[item.category] || '/assets/hero.svg';
                })()}
                alt={item.category}
              />
              <div className="rec-body">
                <div className="rec-title">{item.category}</div>
                <div className="rec-meta">₹{item.price} • <span className="tag">{item.occasion}</span></div>
                <div className="score">{score}% Match</div>
                <a className="btn primary" href={link} target="_blank" rel="noreferrer">Shop on Myntra</a>
              </div>
            </div>
          )
        })}
      </div>
    </main>
  )
}
