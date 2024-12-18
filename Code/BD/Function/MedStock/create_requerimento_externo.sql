CREATE OR REPLACE FUNCTION create_requerimento_externo(
    user_id_pedido INT,
    paciente_nome VARCHAR,
    paciente_estado VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
    new_requerimento_id INT;
    new_requerimento_externo_id INT;
BEGIN
    IF paciente_nome IS NULL OR TRIM(paciente_nome) = '' THEN
        RAISE EXCEPTION 'O nome do paciente não pode ser vazio.';
    END IF;

    IF paciente_estado IS NULL OR TRIM(paciente_estado) = '' THEN
        RAISE EXCEPTION 'O estado do paciente não pode ser vazio.';
    END IF;

    INSERT INTO Requerimento (user_id_pedido, urgente, tipo_requerimento)
    VALUES (user_id_pedido, TRUE, 'Externo')
    RETURNING requerimento_id INTO new_requerimento_id;

    INSERT INTO HistoricoRequerimento (requerimento_id, data_modificacao, status, descricao, user_id_responsavel)
    VALUES (new_requerimento_id, CURRENT_TIMESTAMP(0), 11, 'Requerimento externo criado', user_id_pedido);

    INSERT INTO Requerimento_Externo (paciente_nome, paciente_estado, requerimento_id, data_criacao, status)
    VALUES (paciente_nome, paciente_estado, new_requerimento_id, CURRENT_TIMESTAMP(0), 0)
    RETURNING requerimento_externo_id INTO new_requerimento_externo_id;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao criar requerimento externo: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
