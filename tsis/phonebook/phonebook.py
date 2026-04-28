from connect import db_connect


import csv
import json
import os
from connect import db_connect

def insert_from_csv(path="./contacts.csv"):
    conn = db_connect()
    cur = conn.cursor()
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Insert contact
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    row.get("first_name"),
                    row.get("last_name"),
                    row.get("email"),
                    row.get("birthday") or None,
                    row.get("group_id") or None,
                ))
                contact_id = cur.fetchone()[0]

                # Insert phones if phones.csv exists
                phones_path = "./phones.csv"
                if os.path.exists(phones_path):
                    with open(phones_path, newline="", encoding="utf-8") as pf:
                        phones_reader = csv.DictReader(pf)
                        for phone_row in phones_reader:
                            if int(phone_row.get("contact_id", 0)) == contact_id:
                                cur.execute("""
                                    INSERT INTO phones (contact_id, phone, type)
                                    VALUES (%s, %s, %s)
                                """, (
                                    contact_id,
                                    phone_row.get("phone"),
                                    phone_row.get("type"),
                                ))

        conn.commit()
        print("  ✓  CSV imported successfully.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def init_schema():
    conn = db_connect()
    cur = conn.cursor()
    try:
        # Execute schema.sql
        with open('schema.sql', 'r') as f:
            cur.execute(f.read())
        # Execute procedures.sql
        with open('procedures.sql', 'r') as f:
            cur.execute(f.read())
        # Execute functions.sql
        with open('functions.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()
        print("  ✓  Schema, procedures, and functions applied successfully.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_name = input("Enter group name (Family, Work, Friend, Other): ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name ILIKE %s
            GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        """, (group_name,))
        rows = cur.fetchall()
        if rows:
            print(f"\nContacts in group '{group_name}':")
            for row in rows:
                print(f"  {row[0]} {row[1] or ''} | {row[2] or ''} | {row[3] or ''} | {row[4] or ''} | Phones: {row[5] or ''}")
        else:
            print(f"  No contacts found in group '{group_name}'.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def search_by_email():
    query = input("Enter email search query: ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        """, ('%' + query + '%',))
        rows = cur.fetchall()
        if rows:
            print(f"\nContacts with email matching '{query}':")
            for row in rows:
                print(f"  {row[0]} {row[1] or ''} | {row[2] or ''} | {row[3] or ''} | {row[4] or ''} | Phones: {row[5] or ''}")
        else:
            print(f"  No contacts found with email matching '{query}'.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def sort_and_list():
    sort_by = input("Sort by (name, birthday, date): ").strip().lower()
    order_map = {'name': 'c.first_name, c.last_name', 'birthday': 'c.birthday', 'date': 'c.created_at'}
    order = order_map.get(sort_by, 'c.first_name')
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            ORDER BY {order}
        """)
        rows = cur.fetchall()
        if rows:
            print(f"\nAll contacts sorted by {sort_by}:")
            for row in rows:
                print(f"  {row[0]} {row[1] or ''} | {row[2] or ''} | {row[3] or ''} | {row[4] or ''} | Phones: {row[5] or ''}")
        else:
            print("  No contacts found.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def paginated_browse():
    page_size = 5
    page = 0
    conn = db_connect()
    cur = conn.cursor()
    try:
        while True:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, page * page_size))
            rows = cur.fetchall()
            if not rows:
                print("  No more contacts.")
                break
            print(f"\nPage {page + 1}:")
            for row in rows:
                print(f"  ID: {row[0]} | {row[1]} {row[2] or ''} | {row[3] or ''} | {row[4] or ''} | {row[5] or ''} | Phones: {row[6] or ''}")
            choice = input("  (n)ext, (p)rev, (q)uit: ").strip().lower()
            if choice == 'n':
                page += 1
            elif choice == 'p' and page > 0:
                page -= 1
            elif choice == 'q':
                break
            else:
                print("  Invalid choice.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def export_to_json():
    filename = input("Enter JSON filename (e.g., contacts.json): ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name,
                   JSON_AGG(JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type)) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        """)
        rows = cur.fetchall()
        contacts = []
        for row in rows:
            contact = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'birthday': row[4].isoformat() if row[4] else None,
                'group': row[5],
                'phones': row[6] if row[6] else []
            }
            contacts.append(contact)
        with open(filename, 'w') as f:
            json.dump(contacts, f, indent=4)
        print(f"  ✓  Exported {len(contacts)} contacts to {filename}.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def import_from_json():
    filename = input("Enter JSON filename: ").strip()
    if not os.path.exists(filename):
        print(f"  ✗  File {filename} not found.")
        return
    conn = db_connect()
    cur = conn.cursor()
    try:
        with open(filename, 'r') as f:
            contacts = json.load(f)
        for contact in contacts:
            # Check for duplicate by name
            cur.execute("SELECT id FROM contacts WHERE first_name = %s AND last_name = %s", (contact['first_name'], contact.get('last_name')))
            existing = cur.fetchone()
            if existing:
                choice = input(f"  Contact {contact['first_name']} {contact.get('last_name', '')} exists. (s)kip or (o)verwrite? ").strip().lower()
                if choice == 's':
                    continue
                elif choice == 'o':
                    cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
            # Insert contact
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                RETURNING id
            """, (
                contact['first_name'],
                contact.get('last_name'),
                contact.get('email'),
                contact.get('birthday'),
                contact.get('group')
            ))
            contact_id = cur.fetchone()[0]
            # Insert phones
            for phone in contact.get('phones', []):
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (contact_id, phone['phone'], phone['type']))
        conn.commit()
        print(f"  ✓  Imported {len(contacts)} contacts from {filename}.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def call_add_phone():
    contact_name = input("Enter contact name (first last): ").strip()
    phone = input("Enter phone number: ").strip()
    phone_type = input("Enter phone type (home, work, mobile): ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
        conn.commit()
        print("  ✓  Phone added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def call_move_to_group():
    contact_name = input("Enter contact name (first last): ").strip()
    group_name = input("Enter group name: ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        conn.commit()
        print("  ✓  Contact moved to group successfully.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


def call_search_contacts():
    query = input("Enter search query: ").strip()
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
        if rows:
            print(f"\nContacts matching '{query}':")
            for row in rows:
                print(f"  ID: {row[0]} | {row[1]} {row[2] or ''} | {row[3] or ''} | {row[4] or ''} | {row[5] or ''} | Phones: {row[6] or ''}")
        else:
            print(f"  No contacts found matching '{query}'.")
    except Exception as e:
        print(f"  ✗  Error: {e}")
    finally:
        cur.close()
        conn.close()


MENU = """
╔══════════════════════════════════════════════════╗
║         PhoneBook  –  TSIS 1 Extended Menu       ║
╠══════════════════════════════════════════════════╣
║  SCHEMA                                          ║
║  0.  Apply schema & procedures                   ║
╠══════════════════════════════════════════════════╣
║  SEARCH & FILTER                                 ║
║  1.  Filter contacts by group                    ║
║  2.  Search by email                             ║
║  3.  List all contacts (sorted)                  ║
║  4.  Browse contacts (paginated)                 ║
╠══════════════════════════════════════════════════╣
║  IMPORT / EXPORT                                 ║
║  5.  Export to JSON                              ║
║  6.  Import from JSON                            ║
║  7.  Import from CSV (extended)                  ║
╠══════════════════════════════════════════════════╣
║  STORED PROCEDURES                               ║
║  8.  Add phone number to contact                 ║
║  9.  Move contact to group                       ║
║  10. Search contacts (all fields + phones)       ║
╠══════════════════════════════════════════════════╣
║  Q.  Quit                                        ║
╚══════════════════════════════════════════════════╝
"""

HANDLERS = {
    "0":  init_schema,
    "1":  filter_by_group,
    "2":  search_by_email,
    "3":  sort_and_list,
    "4":  paginated_browse,
    "5":  export_to_json,
    "6":  import_from_json,
    "7":  insert_from_csv,
    "8":  call_add_phone,
    "9":  call_move_to_group,
    "10": call_search_contacts,
}

def main():
    while True:
        print(MENU)
        choice = input("Select option: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        handler = HANDLERS.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"  ✗  Database error: {e}")
        else:
            print("  Invalid choice, please try again.")


if __name__ == "__main__":
    main()

# conn.close()
