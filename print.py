import sqlite3
conn = sqlite3.connect('SQL.db')
curs = conn.cursor()


curs.execute('''SELECT * FROM USER''')
rows = curs.fetchall()
print(rows)
curs.execute('''SELECT * FROM BOOK''')
rows = curs.fetchall()
print(rows)
curs.execute('''SELECT * FROM BORROW''')
rows = curs.fetchall()
print(rows)

conn.commit()
curs.close()
conn.close()
