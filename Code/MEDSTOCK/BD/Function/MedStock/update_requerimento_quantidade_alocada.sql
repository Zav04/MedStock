CREATE OR REPLACE FUNCTION update_requerimento_quantidade_alocada(
    p_requerimento_id BIGINT,
    p_consumiveis JSON
)
RETURNS BOOLEAN AS $$
DECLARE
    consumivel JSON;
BEGIN
    IF json_array_length(p_consumiveis) = 0 THEN
        RAISE EXCEPTION 'A lista de consumíveis está vazia.';
    END IF;

    FOR consumivel IN SELECT * FROM json_array_elements(p_consumiveis) LOOP
        UPDATE Consumivel_Requerimento
        SET quantidade_alocada = (consumivel->>'quantidade_alocada')::BIGINT
        WHERE requerimento_id = p_requerimento_id
          AND consumivel_id = (consumivel->>'consumivel_id')::BIGINT;
    END LOOP;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao atualizar quantidades alocadas: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
