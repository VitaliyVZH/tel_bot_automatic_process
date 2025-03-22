import os
import telebot
from telebot import types
from dotenv import load_dotenv
from keyboards.buttons import get_buttons_employees_role

from logs.logger_config import logger


load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN_BOT"))


@bot.message_handler(commands=['start'])
def main(message):
    logger.info(f"Команда /start получена от пользователя: {message.chat.id}")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = get_buttons_employees_role()
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "Выберите роль:", reply_markup=keyboard)


if __name__ == '__main__':
    # Запускаем бота
    try:
        logger.info("Бот запущен...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error("Произошла ошибка: %s", e)
