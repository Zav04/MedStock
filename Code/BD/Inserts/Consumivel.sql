INSERT INTO consumivel (nome_consumivel, tipo_id, codigo, quantidade_total) 
VALUES 
    ('Brufen', 1, MD5(RANDOM()::TEXT), 350),
    ('Paracetamol', 1, MD5(RANDOM()::TEXT), 280),
    ('Aspirina', 1, MD5(RANDOM()::TEXT), 450),
    ('Ibuprofeno', 1, MD5(RANDOM()::TEXT), 375),
    ('Amoxicilina', 1, MD5(RANDOM()::TEXT), 120),
    ('Claritromicina', 1, MD5(RANDOM()::TEXT), 300),
    ('Dipirona', 1, MD5(RANDOM()::TEXT), 250),
    ('Omeprazol', 1, MD5(RANDOM()::TEXT), 400),
    ('Diclofenaco', 1, MD5(RANDOM()::TEXT), 410),
    ('Metformina', 1, MD5(RANDOM()::TEXT), 325);

INSERT INTO consumivel (nome_consumivel, tipo_id, codigo, quantidade_total) 
VALUES 
    ('Vacina COVID-19', 2, MD5(RANDOM()::TEXT), 150),
    ('Vacina Gripe', 2, MD5(RANDOM()::TEXT), 220),
    ('Vacina Hepatite B', 2, MD5(RANDOM()::TEXT), 370),
    ('Vacina Meningite', 2, MD5(RANDOM()::TEXT), 490),
    ('Vacina Sarampo', 2, MD5(RANDOM()::TEXT), 280),
    ('Vacina Varicela', 2, MD5(RANDOM()::TEXT), 340),
    ('Vacina Febre Amarela', 2, MD5(RANDOM()::TEXT), 420),
    ('Vacina HPV', 2, MD5(RANDOM()::TEXT), 470),
    ('Vacina Tétano', 2, MD5(RANDOM()::TEXT), 260),
    ('Vacina Raiva', 2, MD5(RANDOM()::TEXT), 240);

INSERT INTO consumivel (nome_consumivel, tipo_id, codigo, quantidade_total) 
VALUES 
    ('Seringa', 3, MD5(RANDOM()::TEXT), 300),
    ('Compressa Estéril', 3, MD5(RANDOM()::TEXT), 200),
    ('Cateter', 3, MD5(RANDOM()::TEXT), 280),
    ('Agulha Hipodérmica', 3, MD5(RANDOM()::TEXT), 480),
    ('Luvas Descartáveis', 3, MD5(RANDOM()::TEXT), 370),
    ('Máscara Cirúrgica', 3, MD5(RANDOM()::TEXT), 410),
    ('Bisturi', 3, MD5(RANDOM()::TEXT), 320),
    ('Esparadrapo', 3, MD5(RANDOM()::TEXT), 450),
    ('Sonda Nasogástrica', 3, MD5(RANDOM()::TEXT), 380),
    ('Tubo Endotraqueal', 3, MD5(RANDOM()::TEXT), 230);


INSERT INTO consumivel (nome_consumivel, tipo_id, codigo, quantidade_total) 
VALUES 
    ('Gaze', 4, MD5(RANDOM()::TEXT), 270),
    ('Solução Fisiológica', 4, MD5(RANDOM()::TEXT), 390),
    ('Álcool 70%', 4, MD5(RANDOM()::TEXT), 220),
    ('Termômetro', 4, MD5(RANDOM()::TEXT), 420),
    ('Oxímetro', 4, MD5(RANDOM()::TEXT), 350);
