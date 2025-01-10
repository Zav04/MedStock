CREATE OR REPLACE FUNCTION create_utilizador(
    p_nome VARCHAR(255),
    p_email VARCHAR(255),
    p_sexo CHAR(1),
    p_data_nascimento DATE,
    p_role_id BIGINT
)
RETURNS BOOLEAN AS $$
DECLARE
BEGIN

    IF p_nome IS NULL OR LENGTH(p_nome) < 3 THEN
        RAISE EXCEPTION 'O nome deve ter pelo menos 3 caracteres e não pode estar vazio.';
    END IF;

    IF p_email IS NULL OR NOT p_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'O email fornecido não é válido.';
    END IF;
    
    IF verify_exist_email(p_email) THEN
        RAISE EXCEPTION 'O email % já foi registrado.', p_email;
    END IF;

    IF p_sexo IS NULL OR NOT p_sexo IN ('M', 'F') THEN
        RAISE EXCEPTION 'O sexo fornecido não é válido';
    END IF;

    IF p_data_nascimento IS NULL OR p_data_nascimento > CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de nascimento não pode ser vazia e deve ser anterior ou igual à data atual.';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM "role" WHERE role_id = p_role_id) THEN
        RAISE EXCEPTION 'O Cargo fornecido não existe';
    END IF;

    INSERT INTO utilizador (nome, email, sexo, data_nascimento, role_id)
    VALUES (p_nome, p_email, p_sexo, p_data_nascimento, p_role_id);
    
    RETURN true;
END;
$$ LANGUAGE plpgsql;
