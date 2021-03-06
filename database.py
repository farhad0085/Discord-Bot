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
    # print(values)
    conn = sqlite3.connect('messages.sqlite')
    curr = conn.cursor()
    curr.execute('''insert into message ("name", "message", "channel", "datetime") VALUES (?,?,?,?)''', values)
    conn.commit()

def get_all_messages():
    messages = curr.execute('''SELECT * from message''')
    output = []
    for message in messages:
        output.append(list(message))

    return output

if __name__ == "__main__":
    msgs = get_all_messages()