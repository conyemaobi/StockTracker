import psycopg2

cur = conn.cursor()
cur.execute("DELETE FROM STOCKS")
conn.commit()
