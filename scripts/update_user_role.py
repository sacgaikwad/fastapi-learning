import sqlite3

db_path = r"D:\Learning\Python\fastapi-learning\data\app.db"

connection = sqlite3.connect(db_path)

cursor = connection.cursor()

cursor.execute("""
    UPDATE users
    SET role = ?
    WHERE id = ?
""", ("ADMIN", 1))

connection.commit()

cursor.execute("""
    SELECT id, name, email, role
    FROM users
    WHERE id = ?
""", (1,))

print(cursor.fetchone())

connection.close()