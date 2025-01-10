CREATE OR REPLACE FUNCTION update_utilizador_to_setor(
    p_utilizador_id BIGINT,
    p_setor_id BIGINT
) RETURNS BOOLEAN AS $$
DECLARE
    setor_exists INT;
    utilizador_exists INT;
    gestor_role_id INT;
BEGIN

    SELECT COUNT(*) INTO setor_exists
    FROM Setor_Hospital
    WHERE setor_id = p_setor_id;

    IF setor_exists = 0 THEN
        RAISE EXCEPTION 'Setor com ID % não encontrado.', p_setor_id;
    END IF;

    SELECT COUNT(*) INTO utilizador_exists
    FROM Utilizador
    WHERE utilizador_id = p_utilizador_id;

    IF utilizador_exists = 0 THEN
        RAISE EXCEPTION 'Utilizador com ID % não encontrado.', p_utilizador_id;
    END IF;

    SELECT role_id INTO gestor_role_id
    FROM Role
    WHERE nome_role = 'Gestor Responsável';

    IF gestor_role_id IS NULL THEN
        RAISE EXCEPTION 'Role "Gestor Responsável" não encontrada.';
    END IF;

    UPDATE Setor_Hospital
    SET responsavel_id = p_utilizador_id
    WHERE setor_id = p_setor_id;

    UPDATE Utilizador
    SET role_id = gestor_role_id
    WHERE utilizador_id = p_utilizador_id;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao associar utilizador ao setor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;