import sqlite3
from telebot import types
from database.db_manager import Database
from logs.logger_config import logger


def get_buttons_employees_role():
    db = Database()
    db.connect()
    try:
        roles = db.get_employee_roles()
        buttons = [types.KeyboardButton(role) for role in roles]
        return buttons
    except sqlite3.Error as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        return []
    finally:
        db.close()
