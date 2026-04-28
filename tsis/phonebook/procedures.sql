CREATE OR REPLACE PROCEDURE insert_person(
    p_table_name  TEXT,
    p_first_name  VARCHAR(50),
    p_last_name   VARCHAR(50),
    p_email       VARCHAR(100),
    p_birthday    DATE,
    p_group_id    INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format(
        'INSERT INTO %I (first_name, last_name, email, birthday, group_id)
         VALUES ($1, $2, $3, $4, $5)',
        p_table_name
    )
    USING p_first_name, p_last_name, p_email, p_birthday, p_group_id;
END;
$$;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Find contact by first_name (assuming unique, or use full name)
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name || ' ' || COALESCE(last_name, '') = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    -- Find contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name || ' ' || COALESCE(last_name, '') = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    -- Find or create group
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;