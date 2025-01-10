CREATE OR REPLACE FUNCTION update_consumivel(
    p_consumivel_id INTEGER,
    p_quantidade_minima INTEGER,
    p_quantidade_pedido INTEGER
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE consumivel
    SET 
        quantidade_minima = p_quantidade_minima,
        quantidade_pedido = p_quantidade_pedido
    WHERE consumivel_id = p_consumivel_id;

    IF FOUND THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;
