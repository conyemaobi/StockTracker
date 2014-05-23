import psycopg2
import passwords

conn = psycopg2.connect(database=passwords.Live.database, user=passwords.Live.user, password=passwords.Live.password, host=passwords.Live.host, port=passwords.Live.port)
cur = conn.cursor()
cur.execute("DELETE FROM STOCKS")
conn.commit()
