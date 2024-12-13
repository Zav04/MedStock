CREATE OR REPLACE FUNCTION create_consumivel(
    p_nome_consumivel VARCHAR,
    p_codigo VARCHAR,
    p_tipo_id INT
) RETURNS BOOLEAN AS $$
BEGIN
    IF p_nome_consumivel IS NULL OR TRIM(p_nome_consumivel) = '' THEN
        RAISE EXCEPTION 'O nome do consumível é obrigatório.';
    END IF;

    IF p_codigo IS NULL OR TRIM(p_codigo) = '' THEN
        RAISE EXCEPTION 'O código do consumível é obrigatório.';
    END IF;

    IF LENGTH(p_codigo) <> 33 THEN
        RAISE EXCEPTION 'O código do consumível deve ter exatamente 33 caracteres.';
    END IF;

    IF p_tipo_id IS NULL OR p_tipo_id <= 0 THEN
        RAISE EXCEPTION 'O tipo do consumível é obrigatório e deve ser um ID válido.';
    END IF;

    INSERT INTO Consumivel (
        nome_consumivel,
        codigo,
        tipo_id,
        quantidade_total,
        quantidade_minima
    ) VALUES (
        p_nome_consumivel,
        p_codigo,
        p_tipo_id,
        0,
        0
    );

    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao inserir consumível: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
