import sqlite3


def create_connection():
    """Создание соединения с базой данных, если БД не существует, тогда БД создастся"""
    conn = sqlite3.connect("task.db")
    return conn


def create_tables():
    """Создание таблиц"""
    conn = create_connection()
    cursor = conn.cursor()

    # Создание таблицы подразделений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50) NOT NULL UNIQUE)''')

    # Создание таблицы с должностями
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL UNIQUE)
    ''')

    # Создание таблицы с работниками
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(250) NOT NULL,
    position_id INTEGER,
    FOREIGN KEY (position_id) REFERENCES positions(id))
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
