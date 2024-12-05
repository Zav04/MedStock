CREATE OR REPLACE FUNCTION get_user_by_email(user_email VARCHAR)
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
        u.role_id,
        r.nome_role
    FROM 
        Utilizador u
    INNER JOIN 
        Role r ON u.role_id = r.role_id
    WHERE 
        u.email = user_email;
END;
$$ LANGUAGE plpgsql;