import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def db_connect():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def get_or_create_player(username):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()
    if not player:
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
    else:
        player_id = player[0]
    cur.close()
    conn.close()
    return player_id

def save_game_session(player_id, score, level_reached):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level_reached))
    conn.commit()
    cur.close()
    conn.close()

def get_top_scores():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    top_scores = cur.fetchall()
    cur.close()
    conn.close()
    return top_scores

def get_personal_best(player_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    pb = cur.fetchone()[0]
    cur.close()
    conn.close()
    return pb or 0