import axios from 'axios';

// URL base da API Flask
const API_URL = 'http://localhost:5000/api';

/**
 * Função utilitária para tratar erros da API.
 * @param {Object} error - Objeto de erro lançado pelo Axios.
 * @param {string} customMessage - Mensagem personalizada para o erro.
 */
const handleApiError = (error, customMessage) => {
  if (error.response) {
    console.error(`${customMessage}:`, error.response.data);
    console.error(`Status Code: ${error.response.status}`);
    throw new Error(error.response.data.message || `${customMessage}: Erro desconhecido na API`);
  } else if (error.request) {
    console.error(`${customMessage}: Erro de solicitação`, error.request);
    throw new Error(`${customMessage}: Sem resposta da API`);
  } else {
    console.error(`${customMessage}:`, error.message);
    throw new Error(`${customMessage}: ${error.message}`);
  }
};

/**
 * Busca todos os fornecedores.
 * @returns {Promise<Array>} Lista de fornecedores.
 */
export const getFornecedores = async () => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores`);
    return response.data; // Retorna os dados dos fornecedores.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar fornecedores');
  }
};

/**
 * Busca os requerimentos agrupados por estado para todos os fornecedores.
 * @returns {Promise<Object>} Requerimentos agrupados por estado e fornecedor.
 */
export const getRequerimentosAgrupados = async () => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/requerimentos`);
    return response.data; // Retorna os dados agrupados por fornecedor.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar requerimentos agrupados');
  }
};

/**
 * Busca os produtos de um fornecedor específico.
 * Retorna os produtos e a quantidade total de produtos disponíveis.
 * @param {number} fornecedorId - ID do fornecedor.
 * @returns {Promise<Object>} Produtos e quantidade total de produtos.
 */
export const getProdutosPorFornecedor = async (fornecedorId) => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/${fornecedorId}/produtos`);
    const produtos = response.data.produtos;

    // Calcula a quantidade total de produtos
    const quantidadeTotal = produtos.reduce((total, produto) => total + produto.quantidade, 0);

    return {
      fornecedor: response.data.fornecedor,
      produtos,
      quantidade: quantidadeTotal, // Quantidade total de produtos disponíveis
    };
  } catch (error) {
    handleApiError(error, 'Erro ao buscar produtos do fornecedor');
  }
};

/**
 * Busca os requerimentos em espera de um fornecedor específico.
 * @param {number} fornecedorId - ID do fornecedor.
 * @returns {Promise<Array>} Requerimentos em espera.
 */
export const getRequerimentosEmEspera = async (fornecedorId) => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/${fornecedorId}/requerimentos/em_espera`);
    return response.data; // Retorna os dados dos requerimentos em espera.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar requerimentos em espera');
  }
};


/**
 * Busca os requerimentos em espera de um fornecedor específico.
 * @param {number} fornecedorId - ID do fornecedor.
 * @returns {Promise<Array>} Requerimentos em preparação.
 */
export const getRequerimentosEnviado = async (fornecedorId) => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/${fornecedorId}/requerimentos/enviado`);
    return response.data; // Retorna os dados dos requerimentos em espera.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar requerimentos enviados');
  }
};

/**
 * Busca os requerimentos em espera de um fornecedor específico.
 * @param {number} fornecedorId - ID do fornecedor.
 * @returns {Promise<Array>} Requerimentos enviados.
 */
export const getRequerimentosFinalizado = async (fornecedorId) => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/${fornecedorId}/requerimentos/finalizado`);
    return response.data; // Retorna os dados dos requerimentos em espera.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar requerimentos finalizados');
  }
};


/**
 * Busca os requerimentos em espera de um fornecedor específico.
 * @param {number} fornecedorId - ID do fornecedor.
 * @returns {Promise<Array>} Requerimentos finalizados.
 */
export const getRequerimentosEmPreparacao = async (fornecedorId) => {
  try {
    const response = await axios.get(`${API_URL}/fornecedores/${fornecedorId}/requerimentos/em_preparacao`);
    return response.data; // Retorna os dados dos requerimentos em espera.
  } catch (error) {
    handleApiError(error, 'Erro ao buscar requerimentos em preparação');
  }
};



/**
 * Atualiza o estado de um requerimento.
 * @param {number} idRequerimento - ID do requerimento.
 * @param {string} novoEstado - Novo estado do requerimento.
 */
// Atualiza o estado de um requerimento
export const updateRequerimentoEstado = async (idRequerimento, novoEstado) => {
  try {
    console.log("Enviando requisição...");
    const response = await axios.put(`${API_URL}/requerimentos/${idRequerimento}/estado`, 
    {
      estado: novoEstado
    }, 
    {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log("Resposta da API:", response.data);
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar estado do requerimento:", error.message);
    throw error;
  }
};


/**
 * Finaliza um requerimento e atualiza as quantidades dos produtos no estoque.
 * @param {number} requerimentoId - ID do requerimento a ser finalizado.
 * @param {Array} produtosQuantidades - Lista de produtos e suas quantidades para subtração.
 * @returns {Promise<Object>} Resposta da API após finalizar o requerimento.
 */
export const finalizarRequerimento = async (requerimentoId, produtosQuantidades) => {
  try {
    // Enviando a requisição PUT para finalizar o requerimento
    const response = await axios.put(`${API_URL}/requerimentos/${requerimentoId}/finalizar`, 
    {
      produtos: produtosQuantidades, // Lista com {produto_id, quantidade}
    },
    {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log("Resposta da API:", response.data);
    return response.data;
  } catch (error) {
    console.error("Erro ao finalizar requerimento:", error.message);
    throw error;
  }
};

