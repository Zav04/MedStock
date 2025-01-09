// src/components/CardEmEspera.js
import React, { useState, useEffect } from "react";
import { getRequerimentosEmEspera, updateRequerimentoEstado } from "../../services/api";
import "../../styles/Pedidos.css"; // Certifique-se de que o estilo está no arquivo correto

const CardEmEspera = ({ fornecedorId }) => {
  const [requerimentosEmEspera, setRequerimentosEmEspera] = useState([]);
  const [expandedRequerimentos, setExpandedRequerimentos] = useState([]);

  // Função para buscar os requerimentos em espera do fornecedor
  const fetchRequerimentosEmEspera = async () => {
    try {
      const requerimentosData = await getRequerimentosEmEspera(fornecedorId);
      setRequerimentosEmEspera(requerimentosData);
    } catch (error) {
      console.error("Erro ao buscar requerimentos em espera:", error.message);
    }
  };

  // Função para alternar a exibição dos detalhes do requerimento
  const toggleExpandRequerimento = (id) => {
    setExpandedRequerimentos((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  // Função para aceitar o requerimento
  const handleAceitarRequerimento = async (idRequerimento) => {
    try {
      await updateRequerimentoEstado(idRequerimento, "EM PREPARAÇÃO"); // Atualiza o estado para "EM PREPARAÇÃO"
      // Atualiza a lista de requerimentos após a mudança de estado
      setRequerimentosEmEspera((prev) =>
        prev.filter((req) => req.id_requerimento !== idRequerimento)
      );
    } catch (error) {
      console.error("Erro ao aceitar requerimento:", error.message);
    }
  };

  // Usando useEffect para buscar os requerimentos em espera
  useEffect(() => {
    fetchRequerimentosEmEspera();
  }, [fornecedorId]);

  return (
    <div className="requerimentos-container">
      <h2>Requerimentos em Espera</h2>
      {requerimentosEmEspera.length > 0 ? (
        requerimentosEmEspera.map((requerimento) => (
          <div
            key={requerimento.id_requerimento}
            className={`requerimento-box ${
              expandedRequerimentos.includes(requerimento.id_requerimento)
                ? "expandido"
                : ""
            }`}
            onClick={() => toggleExpandRequerimento(requerimento.id_requerimento)}
          >
            {/* Cabeçalho do requerimento */}
            <div className="requerimento-header">
              <h3>Requerimento {requerimento.id_requerimento}</h3>
            </div>

            {/* Detalhes do requerimento */}
            <div className="requerimento-detalhes">
              <ul>
                {requerimento.produtos.map((produto) => (
                  <li key={produto.produto_id}>
                    {produto.produto_nome} - Quantidade: {produto.quantidade_pedida}
                  </li>
                ))}
              </ul>
            </div>

            {/* Botão para aceitar o requerimento */}
            <div className="requerimento-acoes">
              <button
                onClick={(e) => {
                  e.stopPropagation(); // Impede que o clique no botão expanda ou feche o requerimento
                  handleAceitarRequerimento(requerimento.id_requerimento);
                }}
                className="botao-aceitar"
              >
                Aceitar
              </button>
            </div>
          </div>
        ))
      ) : (
        <p>Não há requerimentos em espera.</p>
      )}
    </div>
  );
};

export default CardEmEspera;
