// src/pages/Home.js
import React, { useState, useEffect } from "react";
import { getFornecedores, getRequerimentosAgrupados } from "../../services/api";
import "../../styles/FornecedorCard.css"; // Certifique-se de que o CSS está sendo importado corretamente
import { Link } from "react-router-dom"; // Adicionando o Link

const CardConsumiveis = () => {
  const [fornecedores, setFornecedores] = useState([]);
  const [requerimentosPorFornecedor, setRequerimentosPorFornecedor] = useState(
    {}
  );
  const [erro, setErro] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch fornecedores
  useEffect(() => {
    const fetchFornecedores = async () => {
      try {
        // Buscar todos os fornecedores
        const fornecedoresData = await getFornecedores();

        // Filtra para pegar apenas o fornecedor de vacinas
        const fornecedorVacina = fornecedoresData.find(
          (fornecedor) => fornecedor.categoria === "Outros"
        );

        setFornecedores(fornecedorVacina ? [fornecedorVacina] : []);
        setLoading(false);
      } catch (error) {
        setErro("Erro ao carregar fornecedores");
        setLoading(false);
      }
    };

    fetchFornecedores();
  }, []);

  // Fetch requerimentos agrupados
  useEffect(() => {
    const fetchRequerimentos = async () => {
      try {
        // Busca todos os requerimentos agrupados
        const requerimentosData = await getRequerimentosAgrupados();
        setRequerimentosPorFornecedor(requerimentosData);
      } catch (error) {
        console.error("Erro ao buscar requerimentos agrupados:", error);
      }
    };

    fetchRequerimentos();
  }, []);

  if (loading) {
    return <div className="loading">Carregando...</div>;
  }

  if (erro) {
    return <div className="error">{erro}</div>;
  }

  // Aqui vamos pegar o primeiro fornecedor da lista
  const fornecedor = fornecedores[0] || {};
  const requerimentos = requerimentosPorFornecedor[fornecedor.id] || {
    em_espera: 0,
    em_preparacao: 0,
    enviado: 0,
    finalizado: 0,
  };

  return (
    <div className="grid-container">
      {/* Exibir apenas o primeiro fornecedor */}
      <div key={fornecedor.id} className="grid-item">
        <h2>{fornecedor.nome}</h2>
        <p>Categoria: {fornecedor.categoria}</p>
        <p>Tempo Mínimo: {fornecedor.tempo_min} horas</p>

        {/* Exibir os estados dos requerimentos */}
        <div className="requerimentos">
          <div className="estado em-espera">
            Em Espera: {requerimentos.em_espera}
          </div>
          <div className="estado em-preparacao">
            Em Preparação: {requerimentos.em_preparacao}
          </div>
          <div className="estado enviado">Enviado: {requerimentos.enviado}</div>
          <div className="estado finalizado">
            Finalizado: {requerimentos.finalizado}
          </div>
        </div>
        <Link to={`./Consumiveis`}>Ver Detalhes</Link>
      </div>
    </div>
  );
};

export default CardConsumiveis;
