// src/pages/Home.js
import React from 'react';
import CardVacinas from '../components/CardFornecedores/CardVacinas';
import CardMedicamentos from '../components/CardFornecedores/CardMedicamentos';
import CardDescartaveis from '../components/CardFornecedores/CardDescartaveis';
import CardConsumiveis from '../components/CardFornecedores/CardConsumiveis';
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <div >
        <CardMedicamentos />
      </div>
      <div >
        <CardVacinas />
      </div>
      <div>
        <CardDescartaveis />
      </div>
      <div >
        <CardConsumiveis />
      </div>
    </div>
  );
};

export default Home;
