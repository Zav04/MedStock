
INSERT INTO Medicamentos (nome_medicamento, tipo_id, codigo) 
VALUES 
('Brufen', 1, MD5(RANDOM()::TEXT)),
('Paracetamol', 1, MD5(RANDOM()::TEXT)),
('Aspirina', 1, MD5(RANDOM()::TEXT)),
('Ibuprofeno', 1, MD5(RANDOM()::TEXT)),
('Amoxicilina', 1, MD5(RANDOM()::TEXT)),
('Claritromicina', 1, MD5(RANDOM()::TEXT)),
('Dipirona', 1, MD5(RANDOM()::TEXT)),
('Omeprazol', 1, MD5(RANDOM()::TEXT)),
('Diclofenaco', 1, MD5(RANDOM()::TEXT)),
('Metformina', 1, MD5(RANDOM()::TEXT));


INSERT INTO Medicamentos (nome_medicamento, tipo_id, codigo) 
VALUES 
('Vacina COVID-19', 2, MD5(RANDOM()::TEXT)),
('Vacina Gripe', 2, MD5(RANDOM()::TEXT)),
('Vacina Hepatite B', 2, MD5(RANDOM()::TEXT)),
('Vacina Meningite', 2, MD5(RANDOM()::TEXT)),
('Vacina Sarampo', 2, MD5(RANDOM()::TEXT)),
('Vacina Varicela', 2, MD5(RANDOM()::TEXT)),
('Vacina Febre Amarela', 2, MD5(RANDOM()::TEXT)),
('Vacina HPV', 2, MD5(RANDOM()::TEXT)),
('Vacina Tétano', 2, MD5(RANDOM()::TEXT)),
('Vacina Raiva', 2, MD5(RANDOM()::TEXT));


INSERT INTO Medicamentos (nome_medicamento, tipo_id, codigo) 
VALUES 
('Seringa', 3, MD5(RANDOM()::TEXT)),
('Compressa Estéril', 3, MD5(RANDOM()::TEXT)),
('Cateter', 3, MD5(RANDOM()::TEXT)),
('Agulha Hipodérmica', 3, MD5(RANDOM()::TEXT)),
('Luvas Descartáveis', 3, MD5(RANDOM()::TEXT)),
('Máscara Cirúrgica', 3, MD5(RANDOM()::TEXT)),
('Bisturi', 3, MD5(RANDOM()::TEXT)),
('Esparadrapo', 3, MD5(RANDOM()::TEXT)),
('Sonda Nasogástrica', 3, MD5(RANDOM()::TEXT)),
('Tubo Endotraqueal', 3, MD5(RANDOM()::TEXT));


INSERT INTO Medicamentos (nome_medicamento, tipo_id, codigo) 
VALUES 
('Gaze', 4, MD5(RANDOM()::TEXT)),
('Solução Fisiológica', 4, MD5(RANDOM()::TEXT)),
('Álcool 70%', 4, MD5(RANDOM()::TEXT)),
('Termômetro', 4, MD5(RANDOM()::TEXT)),
('Oxímetro', 4, MD5(RANDOM()::TEXT));
