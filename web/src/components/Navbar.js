import React from 'react';

export default function Navbar({onNavigate, onToggleDark, dark}){
  return (
    <header className={`navbar ${dark? 'dark':''}`}>
      <div className="nav-left">
        <div className="logo" onClick={()=>onNavigate('home')}>Bharat Fashion AI</div>
        <nav className="nav-links">
          <button onClick={()=>onNavigate('men')}>Men</button>
          <button onClick={()=>onNavigate('women')}>Women</button>
          <button onClick={()=>onNavigate('kids')}>Kids</button>
          <button onClick={()=>onNavigate('home')}>Home & Living</button>
          <button onClick={()=>onNavigate('beauty')}>Beauty</button>
          <button onClick={()=>onNavigate('categories')}>Categories</button>
        </nav>
      </div>
      <div className="nav-right">
        <input className="search" placeholder="Search for products, brands and more" />
        <button className="icon">👤</button>
        <button className="icon">♡</button>
        <button className="icon">🛒</button>
        <button className="toggle" onClick={onToggleDark}>{dark? 'Light' : 'Dark'}</button>
      </div>
    </header>
  )
}
