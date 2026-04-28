CREATE OR REPLACE FUNCTION get_contacts_by_pattern()
RETURNS TABLE(
    contact_username VARCHAR,
    contact_first_name VARCHAR,
    contact_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        username,
        first_name,
        phone_number
    FROM
        phonebook
    WHERE
        first_name ILIKE 'a%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_by_pattern2()
RETURNS TABLE(
    contact_username VARCHAR,
    contact_firstname VARCHAR,
    contact_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        username,
        first_name,
        phone_number
    FROM phonebook WHERE phone_number ILIKE '%+770';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name, c.last_name
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE
        c.first_name ILIKE '%' || p_query || '%' OR
        COALESCE(c.last_name, '') ILIKE '%' || p_query || '%' OR
        COALESCE(c.email, '') ILIKE '%' || p_query || '%' OR
        p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name;
END;
$$ LANGUAGE plpgsql;