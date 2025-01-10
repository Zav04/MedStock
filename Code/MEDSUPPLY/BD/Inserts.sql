-- Inserir Fornecedores
INSERT INTO fornecedores (nome, categoria, tempo_min)
VALUES
    ('Fornecedor de Medicamentos', 'Medicamentos', 24),
    ('Fornecedor de Vacinas', 'Vacinas', 48),
    ('Fornecedor de Descartáveis', 'Material Hospitalar', 72),
    ('Fornecedor de Consumíveis', 'Outros', 36);

-- Inserir Produtos - Medicamentos
INSERT INTO produtos (nome, quantidade, fornecedor_id)
VALUES
    ('Brufen', 20000, 1),
    ('Paracetamol', 20000, 1),
    ('Aspirina', 20000, 1),
    ('Ibuprofeno', 20000, 1),
    ('Amoxicilina', 20000, 1),
    ('Claritromicina', 20000, 1),
    ('Dipirona', 20000, 1),
    ('Omeprazol', 20000, 1),
    ('Diclofenaco', 20000, 1),
    ('Metformina', 20000, 1);

-- Inserir Produtos - Vacinas
INSERT INTO produtos (nome, quantidade, fornecedor_id)
VALUES
    ('Vacina COVID-19', 20000, 2),
    ('Vacina Gripe', 20000, 2),
    ('Vacina Hepatite B', 20000, 2),
    ('Vacina Meningite', 20000, 2),
    ('Vacina Sarampo', 20000, 2),
    ('Vacina Varicela', 20000, 2),
    ('Vacina Febre Amarela', 20000, 2),
    ('Vacina HPV', 20000, 2),
    ('Vacina Tétano', 20000, 2),
    ('Vacina Raiva', 20000, 2);

-- Inserir Produtos - Descartáveis
INSERT INTO produtos (nome, quantidade, fornecedor_id)
VALUES
    ('Seringa', 20000, 3),
    ('Compressa Estéril', 20000, 3),
    ('Cateter', 20000, 3),
    ('Agulha Hipodérmica', 20000, 3),
    ('Luvas Descartáveis', 20000, 3),
    ('Máscara Cirúrgica', 20000, 3),
    ('Bisturi', 20000, 3),
    ('Esparadrapo', 20000, 3),
    ('Sonda Nasogástrica', 20000, 3),
    ('Tubo Endotraqueal', 20000, 3);

-- Inserir Produtos - Consumíveis
INSERT INTO produtos (nome, quantidade, fornecedor_id)
VALUES
    ('Gaze', 20000, 4),
    ('Solução Fisiológica', 20000, 4),
    ('Álcool 70%', 20000, 4),
    ('Termômetro', 20000, 4),
    ('Oxímetro', 20000, 4);

