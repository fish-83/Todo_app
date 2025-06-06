import sqlite3

conn = sqlite3.connect('todo.db')
c = conn.cursor()

#tasks テーブルを作成(ない時は新規作成)

c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          completed INTEGER NOT NULL DEFAULT 0,
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print('テーブルが作成されました')