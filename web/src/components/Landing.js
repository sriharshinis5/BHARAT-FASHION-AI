import React from 'react';
import { fashionData } from '../data/fashionData';

export default function Landing({onNavigate}){
  return (
    <main className="container">
      <section className="hero">
        <div className="hero-left">
          <h1>AI-Powered Bharat Fashion AI</h1>
          <p>Discover personalized fashion recommendations based on your occasion, budget and style preferences.</p>
          <div className="hero-cta">
            <button onClick={()=>onNavigate('categories')} className="btn primary">Explore Categories</button>
            <a className="btn outline" href="https://www.myntra.com" target="_blank" rel="noreferrer">Shop on Myntra</a>
          </div>
        </div>
        <div className="hero-right">
          <img alt="hero" src="/assets/hero.svg" />
        </div>
      </section>

      <section className="section">
        <h2>Trending Categories</h2>
        <div className="cards">
          {fashionData.map((f)=> (
            <div key={f.category} className="cat-card">
              <img alt={f.category} src={`/assets/${f.category.toLowerCase()}.svg`} />
              <div className="cat-body">
                <div className="cat-title">{f.category}</div>
                <div className="cat-meta">Starting ₹{f.price} • <span className="tag">{f.occasion}</span></div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="section offers">
        <h2>Featured Offers</h2>
        <div className="offer-grid">
          <div className="offer">Festival Collection</div>
          <div className="offer">Casual Collection</div>
          <div className="offer">Office Wear</div>
          <div className="offer">Winter Collection</div>
          <div className="offer">Party Collection</div>
        </div>
      </section>

      <section className="section why">
        <h2>Why Bharat Fashion AI?</h2>
        <div className="why-grid">
          <div className="why-card">🤖<div>AI Recommendations</div></div>
          <div className="why-card">💸<div>Budget Friendly</div></div>
          <div className="why-card">🎯<div>Occasion Based</div></div>
          <div className="why-card">🔗<div>Direct Myntra Shopping</div></div>
        </div>
      </section>
    </main>
  )
}
