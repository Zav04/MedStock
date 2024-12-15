CREATE OR REPLACE FUNCTION get_utilizadores_com_setores_alocados()
RETURNS TABLE(
    utilizador_id BIGINT,
    nome VARCHAR,
    nome_setor VARCHAR,
    localizacao VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.utilizador_id,
        u.nome,
        s.nome_setor,
        s.localizacao
    FROM 
        Utilizador u
    INNER JOIN 
        Setor_Hospital s ON s.responsavel_id = u.utilizador_id
    WHERE 
        s.responsavel_id IS NOT NULL
    ORDER BY 
        s.nome_setor;
END;
$$ LANGUAGE plpgsql;
