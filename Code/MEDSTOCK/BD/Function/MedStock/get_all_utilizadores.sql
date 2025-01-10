CREATE OR REPLACE FUNCTION get_all_utilizadores()
RETURNS TABLE(
    utilizador_id BIGINT,
    nome VARCHAR,
    email VARCHAR,
    sexo VARCHAR,
    data_nascimento DATE,
    role_id BIGINT,
    role_nome VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.utilizador_id,
        u.nome,
        u.email,
        u.sexo,
        u.data_nascimento,
        r.role_id,
        r.nome_role AS role_nome
    FROM 
        Utilizador u
    LEFT JOIN 
        role r ON u.role_id = r.role_id
    ORDER BY 
        u.nome ASC;
END;
$$ LANGUAGE plpgsql;