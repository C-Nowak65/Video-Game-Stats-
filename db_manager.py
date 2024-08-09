import sqlite3

#Create the tables needed
def create_tables():
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        session_date TEXT, 
        FOREIGN KEY (game_id) REFERENCES games (id)
    )
''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attributes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        attribute_name TEXT,
        attribute_value TEXT,
        FOREiGN KEY (session_id) REFERENCES sessions (id)
    )
''')

    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect('game_stats.db')
