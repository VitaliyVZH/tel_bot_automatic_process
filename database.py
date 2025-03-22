"""В модуле создаются таблицы."""

import sqlite3
from functools import wraps
import logging
from colorama import Fore, Style, init

# Инициализация colorama.
# Меняет цвет логов.
init(autoreset=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)


def control_create_tables(func):
    """Логирование создания таблиц."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{Fore.GREEN}Создание таблицы: {func.__name__}")
        try:
            res = func(*args, **kwargs)
            logger.info(f"{Fore.GREEN}Таблица {func.__name__} успешно создана.{Style.RESET_ALL}\n")
            return res
        except sqlite3.Error as e:
            logger.warning(f"{Fore.RED}Ошибка при создании таблицы {func.__name__}: {e}\n")
            logger.warning(f"SQL ошибка: {e.args[0]}")  # Выводим конкретную ошибку
        except Exception as e:
            logger.warning(f"{Fore.RED}Неизвестная ошибка при создании таблицы {func.__name__}: {e}")

    return wrapper


@control_create_tables
def create_departament_table(cursor):
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
    departament_id INTEGER NOT NULL,
    FOREIGN KEY (departament_id) REFERENCES department(id) ON DELETE CASCADE)
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
    departament_id INTEGER NOT NULL,
    employee_roles_id INTEGER NOT NULL,
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (departament_id) REFERENCES department(id),
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
    departament_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (departament_id) REFERENCES departament(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
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
    departament_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (departament_id) REFERENCES departament(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id))''')


def create_connection():
    """Создание соединения с базой данных, если БД не существует, тогда БД создастся."""
    conn = sqlite3.connect("task.db")
    return conn


def create_tables():
    """Создание таблиц."""
    # Создаём соединение с БД
    conn = create_connection()
    cursor = conn.cursor()

    create_departament_table(cursor)
    create_employee_position_table(cursor)
    create_employee_roles_table(cursor)
    create_employee_table(cursor)
    create_task_table(cursor)
    create_task_history_table(cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
