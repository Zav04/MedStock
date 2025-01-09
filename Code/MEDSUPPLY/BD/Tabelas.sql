CREATE TABLE fornecedores (
    id_fornecedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    tempo_min INT NOT NULL
);

-- Tabela Produto
CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    quantidade INT NOT NULL,
    fornecedor_id INT NOT NULL,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id_fornecedor)
);

-- Tabela Requerimentos
CREATE TABLE requerimentos (
    id_rquerimento INT PRIMARY KEY,
    fornecedor_id INT NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('EM ESPERA', 'EM PREPARAÇÃO', 'ENVIADO', 'FINALIZADO')) NOT NULL,
    data TIMESTAMP DEFAULT NOW(), 
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id_fornecedor)
);


-- Tabela Pedidos
CREATE TABLE pedidos (
    requerimento_id INT NOT NULL,
    produto_id INT NOT NULL,
    fornecedor_id INT NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (requerimento_id, produto_id, fornecedor_id),
    FOREIGN KEY (requerimento_id) REFERENCES requerimentos (id_requerimento),
    FOREIGN KEY (produto_id) REFERENCES produtos (id_produto),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id_fornecedor)
);

