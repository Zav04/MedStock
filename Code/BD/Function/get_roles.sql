CREATE OR REPLACE FUNCTION get_roles()
RETURNS TABLE(role_id BIGINT, nome_role VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT role.role_id, role.nome_role
    FROM role;
END;
$$ LANGUAGE plpgsql;
