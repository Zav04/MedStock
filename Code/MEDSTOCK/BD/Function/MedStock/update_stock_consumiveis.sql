CREATE OR REPLACE FUNCTION update_stock_consumiveis(
    consumiveis JSON
)
RETURNS BOOLEAN AS $$
DECLARE
    consumivel JSON;
    consumivel_nome VARCHAR;
    consumivel_quantidade INT;
    consumivel_id_var BIGINT;
BEGIN

    IF json_typeof(consumiveis) != 'array' THEN
        RAISE EXCEPTION 'O parâmetro "consumiveis" deve ser um JSON array.';
    END IF;

    FOR consumivel IN SELECT * FROM json_array_elements(consumiveis)
    LOOP
        RAISE NOTICE 'Consumível: %', consumivel;

        consumivel_nome := consumivel->>'nome_consumivel';
        consumivel_quantidade := (consumivel->>'quantidade')::INT;

        IF consumivel_nome IS NULL OR consumivel_quantidade IS NULL THEN
            RAISE EXCEPTION 'Nome ou quantidade do consumível é nulo: %', consumivel;
        END IF;

        SELECT c.consumivel_id
        INTO consumivel_id_var
        FROM Consumivel c
        WHERE c.nome_consumivel = consumivel_nome;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Consumível não encontrado: %', consumivel_nome;
        END IF;

        UPDATE Consumivel
        SET quantidade_total = quantidade_total + consumivel_quantidade
        WHERE consumivel_id = consumivel_id_var;

        RAISE NOTICE 'Estoque atualizado para consumível: %', consumivel_nome;
    END LOOP;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
