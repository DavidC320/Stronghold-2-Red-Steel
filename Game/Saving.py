# 9/21/2022
import sqlite3

database = sqlite3.connect("Database\\test.db")
c = database.cursor()

allies = """create table if not exists
Allies (
    id INTEGER PRIMARY KEY,
    name Text
)"""

c.execute(allies)

for n in range(5):
    c.execute(f"""insert into Allies(name)
    values ({n})
    """)

c.execute("select * from Allies")

print(c.fetchall())