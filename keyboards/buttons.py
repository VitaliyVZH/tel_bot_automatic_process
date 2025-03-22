import sqlite3
from telebot import types
from database.db_manager import Database
from logs.logger_config import logger


def get_buttons_employees_role():
    db = Database()
    db.connect()
    keyboard = types.InlineKeyboardMarkup()
    try:
        # Создаем клавиатуру с кнопками

        roles = db.get_employee_roles()
        for role in roles:
            inline_button = types.InlineKeyboardButton(text=role, callback_data=role)
            keyboard.add(inline_button)
        return keyboard
    except sqlite3.Error as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        return []
    finally:
        db.close()
