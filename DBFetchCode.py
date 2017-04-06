import MySQLdb

conn = MySQLdb.connect(user="root", passwd="gravitant", db="centuriondb")
cur = conn.cursor()

cur.execute("SELECT Error_name FROM ErrorsDict_errorsdict")
row = cur.fetchone()
while row is not None:
    print row[0]
    row = cur.fetchone()

cur.close()
conn.close()