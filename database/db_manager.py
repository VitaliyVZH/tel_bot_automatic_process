import sqlite3
import os
from logs.logger_config import logger


class Database:
    """Класс для доступа к БД."""
    def __init__(self, db_name="task.db"):
        # Получаем путь к корню проекта
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, db_name)
        self.connection = None

    def connect(self):
        """Создание соединения с базой данных."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам по имени
        logger.info(f"Подключено к базе данных: {self.db_path}")

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            self.connection.close()
            logger.info("Соединение с базой данных закрыто.")

    def get_employee_roles(self):
        """Получение списка ролей сотрудников из БД"""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''SELECT * FROM employee_roles''')
            res = [rol["title"] for rol in cursor.fetchall()]
            logger.info("Получение списка ролей сотрудников из БД.")
            return res

    def get_administrator(self) -> bool:
        """Проверка наличия администратора в БД"""
        logger.info("Проверка наличия администратора.")
        self.connect()

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
            SELECT *
            FROM employee_roles
            JOIN employees ON employee_roles.id = employees.employee_roles_id
            WHERE employee_roles.title = 'Администратор'
            ''')

            res = cursor.fetchall()
            if res:
                logger.info("Администратор существует.")
                return True
            logger.info("Администратора нет.")
            return False

    def add_administrator(self, name, last_name, user_tag, user_id, password, email) -> bool:
        """Сохранение администратора в БД"""
        logger.info("Сохранение администратора.")
        self.connect()

        with self.connection:  # Используем контекстный менеджер для автоматического управления транзакциями
            cursor = self.connection.cursor()
            sql = ('''INSERT INTO employees (name, last_name, user_tag, user_id,  password, email, employee_roles_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''')

            try:
                cursor.execute(sql, (name, last_name, user_tag, user_id,  password, email, 1))
                logger.info("Данные успешно добавлены в таблицу.")
                return True
            except sqlite3.IntegrityError:
                logger.info("Ошибка: этот адрес электронной почты уже используется.")
                return False
            except Exception as e:
                logger.error(f"Произошла ошибка: {e}")
                return False
