CREATE OR REPLACE FUNCTION verify_exist_email(email_input VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM Utilizador 
        WHERE email = email_input
    );
END;
$$ LANGUAGE plpgsql;
