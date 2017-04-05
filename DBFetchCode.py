import MySQLdb

conn = MySQLdb.connect(user="user", passwd="password", db="dbname")
cur = conn.cursor()

cur.execute("SELECT id, name FROM students")
row = cur.fetchone()
while row is not None:
    print row[0], row[1]
    row = cur.fetchone()

cur.close()
conn.close()