import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_Password",
    database="echochain_db"
)

cursor = conn.cursor()

print("Connected to MySQL Successfully")

cursor.close()
conn.close()