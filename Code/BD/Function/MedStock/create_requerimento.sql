CREATE OR REPLACE FUNCTION create_requerimento(
    user_id_pedido INT,
    p_setor_id INT,
    items_list JSON,
    urgente BOOLEAN
) RETURNS BOOL AS $$
DECLARE
    new_requerimento_id INT;
    item RECORD;
    setor_responsavel INT;
BEGIN
    IF items_list IS NULL OR json_array_length(items_list) = 0 THEN
        RAISE EXCEPTION 'Selecione pelo menos um item.';
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


    INSERT INTO Requerimento (setor_id, user_id_pedido, data_pedido, status, urgente)
    VALUES (p_setor_id, user_id_pedido, CURRENT_TIMESTAMP(0), 0, urgente)
    RETURNING requerimento_id INTO new_requerimento_id;

    FOR item IN SELECT * FROM json_to_recordset(items_list) AS (item_id INT, quantidade INT)
    LOOP
        INSERT INTO Item_Requerimento (ItemItem_id, Requerimentorequerimento_id, quantidade)
        VALUES (item.item_id, new_requerimento_id, item.quantidade);
    END LOOP;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao criar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
