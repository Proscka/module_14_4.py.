import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()



cursor.execute("DELETE FROM Products")
for num in range(4):
    cursor.execute("INSERT INTO Products(id,title, description,price)VALUE(?,?,?,?)",(f"{num+1}",f"Продукт{num+1}",f"Описание{num+1}",f"{num}get_all_products"))
    connection.commit()

def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INT NOT NULL
        )
        ''')
    connection.commit()

def get_all_products ():
    cursor.execute('SELECT*FROM Products')
    return cursor.fetchall()

connection.commit()
connection.close()