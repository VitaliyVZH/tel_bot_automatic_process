import os
import telebot
from dotenv import load_dotenv
from keyboards.buttons import get_buttons_employees_role
from logs.logger_config import logger
from handlers.handlers import register_role_selection_handlers, register_admin_creation_handler

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN_BOT"))


@bot.message_handler(commands=['start'])
def main(message):
    logger.info(f"Команда /start получена от пользователя: {message.chat.id}")

    keyboard = get_buttons_employees_role()

    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Выберите роль:", reply_markup=keyboard)


if __name__ == '__main__':
    # Регистрируем обработчики
    register_role_selection_handlers(bot)
    register_admin_creation_handler(bot)

    # Запускаем бота
    try:
        logger.info("Бот запущен...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
