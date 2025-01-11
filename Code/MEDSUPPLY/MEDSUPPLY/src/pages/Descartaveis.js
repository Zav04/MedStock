import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/Pedidos.css";
import { getProdutosPorFornecedor } from "../services/api";
import CardEmEspera from "../components/CardEstados/CardEmEspera"; // Importando o novo componente
import CardEmPreparacao from "../components/CardEstados/CardEmPreparacao";
import CardEnviado from "../components/CardEstados/CardEnviado"; // Importando o componente para os requerimentos enviados
import CardFinalizado from "../components/CardEstados/CardFinalizado"; // Importando o componente para os requerimentos finalizados

const Medicamentos = () => {
  const [produtos, setProdutos] = useState([]);
  const [mostrarProdutos, setMostrarProdutos] = useState(false);
  const fornecedorId = 3; // ID do fornecedor de medicamentos

  // Função para buscar os produtos e suas quantidades do fornecedor
  const fetchProdutos = async () => {
    try {
      const produtosData = await getProdutosPorFornecedor(fornecedorId);
      console.log("Produtos retornados:", produtosData); // Log dos produtos
      setProdutos(produtosData.produtos); // Define os produtos no estado
      setMostrarProdutos(!mostrarProdutos); // Alterna a exibição da lista
    } catch (error) {
      console.error("Erro ao buscar produtos:", error.message);
    }
  };

  return (
    <div className="home-container">
      {/* Cabeçalho */}
      <div className="header">
        <h1>Fornecedor de Descartáveis</h1>
        <div>
          <button
            onClick={fetchProdutos}
            style={{ marginRight: "20px" }} // Afastando o botão do link
          >
            {mostrarProdutos ? "Ocultar Produtos" : "Mostrar Produtos"}
          </button>

          <Link to="/" className="botao-voltar-home">
            Voltar para o menú
          </Link>
        </div>
      </div>

      {/* Popup com lista de produtos e quantidades */}
      {mostrarProdutos && (
        <div className="produtos-list">
          <h3>Produtos Disponíveis:</h3>
          <ul>
            {produtos.map((produto) => (
              <li key={produto.id_produto}>
                {produto.nome} - {produto.quantidade}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Exibição dos requerimentos em espera */}
      <CardEmEspera fornecedorId={fornecedorId} />
      <CardEmPreparacao fornecedorId={fornecedorId} />
      <CardEnviado fornecedorId={fornecedorId} />
      <CardFinalizado fornecedorId={fornecedorId} />
    </div>
  );
};

export default Medicamentos;
