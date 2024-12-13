CREATE OR REPLACE FUNCTION create_setor_hospitalar(
    p_nome_setor VARCHAR,
    p_localizacao VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
BEGIN

    IF p_nome_setor IS NULL OR TRIM(p_nome_setor) = '' THEN
        RAISE EXCEPTION 'O nome do setor é obrigatório.';
    END IF;

    IF p_localizacao IS NULL OR TRIM(p_localizacao) = '' THEN
        RAISE EXCEPTION 'A localização do setor é obrigatória.';
    END IF;

    INSERT INTO Setor_Hospital (
        nome_setor,
        localizacao,
        responsavel_id
    ) VALUES (
        p_nome_setor,
        p_localizacao,
        NULL
    );

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao criar o setor hospitalar: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;