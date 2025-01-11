// src/components/CardFinalizado.js
import React, { useState, useEffect } from "react";
import { getRequerimentosFinalizado } from "../../services/api";
import "../../styles/Pedidos.css"; // Certifique-se de que o estilo está no arquivo correto

const CardFinalizado = ({ fornecedorId }) => {
  const [requerimentosFinalizado, setRequerimentosFinalizado] = useState([]);
  const [expandedRequerimentos, setExpandedRequerimentos] = useState([]);

  // Função para buscar os requerimentos finalizados do fornecedor
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchRequerimentosFinalizado = async () => {
    try {
      const requerimentosData = await getRequerimentosFinalizado(fornecedorId);
      setRequerimentosFinalizado(requerimentosData);
    } catch (error) {
      console.error("Erro ao buscar requerimentos finalizados:", error.message);
    }
  };

  // Função para alternar a exibição dos detalhes do requerimento
  const toggleExpandRequerimento = (id) => {
    setExpandedRequerimentos((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  // Usando useEffect para buscar os requerimentos finalizados
  useEffect(() => {
    fetchRequerimentosFinalizado();
  }, [fetchRequerimentosFinalizado, fornecedorId]);

  return (
    <div className="requerimentos-container">
      <h2>Requerimentos Finalizados</h2>
      {requerimentosFinalizado.length > 0 ? (
        requerimentosFinalizado.map((requerimento) => (
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
          </div>
        ))
      ) : (
        <p>Não há requerimentos finalizados.</p>
      )}
    </div>
  );
};

export default CardFinalizado;
