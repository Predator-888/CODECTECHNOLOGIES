import sqlite3

def init_db():
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    # Create table to store chat interactions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_message, bot_response):
    conn = sqlite3.connect('chat_logs.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interactions (user_message, bot_response) VALUES (?, ?)", 
                   (user_message, bot_response))
    conn.commit()
    conn.close()

# Run this file once directly to create the database
if __name__ == '__main__':
    init_db()
    print("Database initialized.")