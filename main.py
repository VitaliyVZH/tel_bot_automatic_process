import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN_BOT"))


@bot.message_handler(commands=['start'])
def main(message):

    bot.send_message(message.chat.id, 'Hello')


if __name__ == '__main__':
    # Запускаем бота
    try:
        print("Бот запущен...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
