CREATE OR REPLACE FUNCTION create_requerimento(
    user_id_pedido INT,
    p_setor_id INT,
    items_list JSON,
    urgente BOOLEAN
) RETURNS BOOLEAN AS $$
DECLARE
    new_requerimento_id INT;
    item RECORD;
    setor_responsavel INT;
BEGIN
    IF items_list IS NULL OR json_array_length(items_list) = 0 THEN
        RAISE EXCEPTION 'Selecione pelo menos um consumível.';
    END IF;

    IF p_setor_id IS NULL THEN
        RAISE EXCEPTION 'Setor não selecionado.';
    END IF;

    SELECT responsavel_id INTO setor_responsavel
    FROM Setor_Hospital
    WHERE setor_id = p_setor_id;

    IF setor_responsavel IS NULL THEN
        RAISE EXCEPTION 'O setor selecionado não possui um responsável definido.';
    END IF;

    INSERT INTO Requerimento (setor_id, user_id_pedido, urgente, tipo_requerimento)
    VALUES (p_setor_id, user_id_pedido, urgente, 'Interno')
    RETURNING requerimento_id INTO new_requerimento_id;

    INSERT INTO HistoricoRequerimento (requerimento_id, data_modificacao, status, descricao, user_id_responsavel)
    VALUES (new_requerimento_id, CURRENT_TIMESTAMP(0), 0, 'Requerimento criado', user_id_pedido);

    FOR item IN SELECT * FROM json_to_recordset(items_list) AS (consumivel_id INT, quantidade INT)
    LOOP
        INSERT INTO Consumivel_Requerimento (consumivel_id, requerimento_id, quantidade)
        VALUES (item.consumivel_id, new_requerimento_id, item.quantidade);
    END LOOP;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao criar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
