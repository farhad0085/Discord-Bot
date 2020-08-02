import sqlite3

conn = sqlite3.connect('messages.sqlite')
curr = conn.cursor()

def create_table():
    create_tables_query = '''
    CREATE TABLE IF NOT EXISTS "message" (
        "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        "name"	TEXT,
        "message"	TEXT,
        "channel"	TEXT,
        "datetime" TEXT
    )
    '''

    curr.executescript(create_tables_query)

def add_message(author, content, channel, time):
    values = (author, content, channel, time)
    print(values)
    conn = sqlite3.connect('messages.sqlite')
    curr = conn.cursor()
    curr.execute('''insert into message ("name", "message", "channel", "datetime") VALUES (?,?,?,?)''', values)
    conn.commit()
