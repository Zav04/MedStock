CREATE OR REPLACE FUNCTION update_requerimento_externo(
    p_requerimento_id INT,
    p_setor_id INT,
    items_list JSON,
    p_user_id INT
) RETURNS BOOLEAN AS $$
DECLARE
    item RECORD;
    setor_responsavel INT;
    descricao_status TEXT;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Requerimento
        WHERE requerimento_id = p_requerimento_id AND tipo_requerimento = 'Externo'
    ) THEN
        RAISE EXCEPTION 'Requerimento Externo não encontrado ou não é do tipo Externo.';
    END IF;

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

    UPDATE Requerimento
    SET setor_id = p_setor_id
    WHERE requerimento_id = p_requerimento_id;

    DELETE FROM Consumivel_Requerimento
    WHERE requerimento_id = p_requerimento_id;

    FOR item IN SELECT * FROM json_to_recordset(items_list) AS (consumivel_id INT, quantidade INT)
    LOOP
        INSERT INTO Consumivel_Requerimento (consumivel_id, requerimento_id, quantidade)
        VALUES (item.consumivel_id, p_requerimento_id, item.quantidade);
    END LOOP;

    descricao_status := 'Requerimento Externo atualizado. Setor e consumíveis modificados. Status alterado para "em preparação".';
    INSERT INTO HistoricoRequerimento (requerimento_id, data_modificacao, status, descricao, user_id_responsavel)
    VALUES (p_requerimento_id, CURRENT_TIMESTAMP(0), 2, descricao_status, p_user_id);

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao atualizar requerimento externo: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


