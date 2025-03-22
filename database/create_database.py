"""В модуле создаются таблицы."""
import os
import sqlite3
from functools import wraps
from logs.logger_config import logger


def control_create_tables(func):
    """Логирование создания таблиц."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Создание таблицы: {func.__name__}")
        try:
            res = func(*args, **kwargs)
            logger.info(f"Таблица {func.__name__} успешно создана.\n")
            return res
        except sqlite3.Error as e:
            logger.warning(f"Ошибка при создании таблицы {func.__name__}: {e}\n")
            logger.warning(f"SQL ошибка: {e.args[0]}")  # Выводим конкретную ошибку
        except Exception as e:
            logger.error(f"Неизвестная ошибка при создании таблицы {func.__name__}: {e}")

    return wrapper


@control_create_tables
def create_department_table(cursor):
    """Создание таблицы подразделений/отделов."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50) NOT NULL UNIQUE)''')


@control_create_tables
def create_employee_position_table(cursor):
    """Создание таблицы с должностями."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE)
    ''')


@control_create_tables
def create_employee_roles_table(cursor):
    """Создание таблицы с ролями сотрудников."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(250) NOT NULL)
    ''')


@control_create_tables
def create_employee_table(cursor):
    """Создание таблицы с работниками."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(250) NOT NULL,
    password VARCHAR(150),
    position_id INTEGER,
    department_id INTEGER NOT NULL,
    employee_roles_id INTEGER NOT NULL,
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (employee_roles_id) REFERENCES employee_roles(id))
    ''')


@control_create_tables
def create_task_table(cursor):
    """Создание таблицы с тасками."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(250) NOT NULL,
    description VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    deadline DATETIME,
    department_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
    )''')


@control_create_tables
def create_task_history_table(cursor):
    """Создание таблицы истории тасок."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(250) NOT NULL,
    description VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    deadline DATETIME,
    department_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id))''')


def create_connection():
    """Создание соединения с базой данных, если БД не существует, тогда БД создастся."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "task.db")
    conn = sqlite3.connect(db_path)
    return conn


def create_tables():
    """Создание таблиц."""
    # Создаём соединение с БД
    with create_connection() as conn:
        cursor = conn.cursor()

    create_department_table(cursor)
    create_employee_position_table(cursor)
    create_employee_roles_table(cursor)
    create_employee_table(cursor)
    create_task_table(cursor)
    create_task_history_table(cursor)


if __name__ == "__main__":
    create_tables()
