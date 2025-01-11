// src/components/CardEmPreparacao.js
import React, { useState, useEffect } from "react";
import {
  getRequerimentosEmPreparacao,
  updateRequerimentoEstado,
} from "../../services/api";
import "../../styles/Pedidos.css"; // Certifique-se de que o estilo está no arquivo correto

const CardEmPreparacao = ({ fornecedorId }) => {
  const [requerimentosEmPreparacao, setRequerimentosEmPreparacao] = useState(
    []
  );
  const [expandedRequerimentos, setExpandedRequerimentos] = useState([]);

  // Função para buscar os requerimentos em preparação do fornecedor
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchRequerimentosEmPreparacao = async () => {
    try {
      const requerimentosData = await getRequerimentosEmPreparacao(
        fornecedorId
      );
      setRequerimentosEmPreparacao(requerimentosData);
    } catch (error) {
      console.error(
        "Erro ao buscar requerimentos em preparação:",
        error.message
      );
    }
  };

  // Função para alternar a exibição dos detalhes do requerimento
  const toggleExpandRequerimento = (id) => {
    setExpandedRequerimentos((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  // Função para marcar o requerimento como "PRONTO"
  const handleMarcarComoPronto = async (idRequerimento) => {
    try {
      await updateRequerimentoEstado(idRequerimento, "ENVIADO"); // Atualiza o estado para "ENVIADO"
      // Atualiza a lista de requerimentos após a mudança de estado
      setRequerimentosEmPreparacao((prev) =>
        prev.filter((req) => req.id_requerimento !== idRequerimento)
      );
    } catch (error) {
      console.error("Erro ao marcar requerimento como pronto:", error.message);
    }
  };

  // Usando useEffect para buscar os requerimentos em preparação
  useEffect(() => {
    fetchRequerimentosEmPreparacao();
  }, [fetchRequerimentosEmPreparacao, fornecedorId]);

  return (
    <div className="requerimentos-container">
      <h2>Requerimentos em Preparação</h2>
      {requerimentosEmPreparacao.length > 0 ? (
        requerimentosEmPreparacao.map((requerimento) => (
          <div
            key={requerimento.id_requerimento}
            className={`requerimento-box ${
              expandedRequerimentos.includes(requerimento.id_requerimento)
                ? "expandido"
                : ""
            }`}
            onClick={() =>
              toggleExpandRequerimento(requerimento.id_requerimento)
            }
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
                    {produto.produto_nome} - Quantidade:{" "}
                    {produto.quantidade_pedida}
                  </li>
                ))}
              </ul>
            </div>

            {/* Botão para marcar como "PRONTO" */}
            <div className="requerimento-acoes">
              <button
                onClick={(e) => {
                  e.stopPropagation(); // Impede que o clique no botão expanda ou feche o requerimento
                  handleMarcarComoPronto(requerimento.id_requerimento);
                }}
                className="botao-aceitar"
              >
                Pronto
              </button>
            </div>
          </div>
        ))
      ) : (
        <p>Não há requerimentos em preparação.</p>
      )}
    </div>
  );
};

export default CardEmPreparacao;
