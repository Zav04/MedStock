import React, { useState, useEffect } from "react";
import { getRequerimentosEnviado, finalizarRequerimento } from "../../services/api"; // Importa a função finalizarRequerimento
import "../../styles/Pedidos.css"; // Certifique-se de que o estilo está no arquivo correto

const CardEnviado = ({ fornecedorId }) => {
  const [requerimentosEnviado, setRequerimentosEnviado] = useState([]);
  const [expandedRequerimentos, setExpandedRequerimentos] = useState([]);

  // Função para buscar os requerimentos enviados do fornecedor
  const fetchRequerimentosEnviado = async () => {
    try {
      const requerimentosData = await getRequerimentosEnviado(fornecedorId);
      setRequerimentosEnviado(requerimentosData);
    } catch (error) {
      console.error("Erro ao buscar requerimentos enviados:", error.message);
    }
  };

  // Função para alternar a exibição dos detalhes do requerimento
  const toggleExpandRequerimento = (id) => {
    setExpandedRequerimentos((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  // Função para marcar o requerimento como "FINALIZADO"
  const handleMarcarComoFinalizado = async (idRequerimento, produtos) => {
    try {
      // Cria um array de objetos contendo produto_id e quantidade
      const produtosQuantidades = produtos.map((produto) => ({
        produto_id: produto.produto_id,
        quantidade: produto.quantidade_pedida,
      }));

      // Usando a função finalizarRequerimento para enviar os dados
      const response = await finalizarRequerimento(idRequerimento, produtosQuantidades);

      // Verifica a resposta e toma ações necessárias
      if (response.message) {
        alert(response.message); // Sucesso
        // Atualiza a lista de requerimentos após a mudança de estado
        setRequerimentosEnviado((prev) =>
          prev.filter((req) => req.id_requerimento !== idRequerimento)
        );
      } else {
        alert(response.error || "Erro ao finalizar requerimento");
      }
    } catch (error) {
      console.error("Erro ao marcar requerimento como finalizado:", error.message);
    }
  };

  // Usando useEffect para buscar os requerimentos enviados
  useEffect(() => {
    fetchRequerimentosEnviado();
  }, [fornecedorId]);

  return (
    <div className="requerimentos-container">
      <h2>Requerimentos Enviados</h2>
      {requerimentosEnviado.length > 0 ? (
        requerimentosEnviado.map((requerimento) => (
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

            {/* Botão para marcar como "FINALIZADO" */}
            <div className="requerimento-acoes">
              <button
                onClick={(e) => {
                  e.stopPropagation(); // Impede que o clique no botão expanda ou feche o requerimento
                  handleMarcarComoFinalizado(
                    requerimento.id_requerimento,
                    requerimento.produtos
                  );
                }}
                className="botao-aceitar"
              >
                Finalizado
              </button>
            </div>
          </div>
        ))
      ) : (
        <p>Não há requerimentos enviados.</p>
      )}
    </div>
  );
};

export default CardEnviado;
