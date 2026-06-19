import React, {useState} from 'react';
import Navbar from './components/Navbar';
import Landing from './components/Landing';
import Recommendations from './components/Recommendations';
import Chatbot from './components/Chatbot';

export default function App(){
  const [page, setPage] = useState('home');
  const [dark, setDark] = useState(false);

  function navigate(p){
    setPage(p);
    window.scrollTo({top:0, behavior:'smooth'});
  }

  return (
    <div className={dark? 'app dark': 'app'}>
      <Navbar onNavigate={navigate} onToggleDark={()=>setDark(d=>!d)} dark={dark} />
      {page==='home' && <Landing onNavigate={navigate} />}
      {page==='categories' && <Recommendations />}
      {page==='ai' && <Chatbot />}
      {page!=='home' && <footer className="footer">
        <div>About Bharat Fashion AI • Privacy Policy • Terms & Conditions • Contact Us</div>
        <div>© 2026 Bharat Fashion AI</div>
      </footer>}

      <button className="to-top" onClick={()=>window.scrollTo({top:0,behavior:'smooth'})}>↑</button>
    </div>
  )
}
