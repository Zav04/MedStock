import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // Certifique-se de ter criado este arquivo
import { BrowserRouter as Router } from 'react-router-dom';  // Para o Router

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>  {/* Envolva o App com Router para que as rotas funcionem */}
      <App />  {/* Renderiza o App, que contém as rotas */}
    </Router>
  </React.StrictMode>
);
