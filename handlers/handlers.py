from loguru import logger


def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        logger.warning(f"Кнопка нажата: {call.data}")

        # Обработка нажатия на кнопку
        if call.data == "Руководитель":
            bot.answer_callback_query(call.id, "Вы выбрали первую роль!")
        elif call.data == "Администратор":
            bot.answer_callback_query(call.id, "Вы выбрали вторую роль!")
        elif call.data == "Подчинённый":
            bot.answer_callback_query(call.id, "Вы выбрали третью роль!")

        bot.send_message(call.message.chat.id, f"Вы нажали кнопку: {call.data}")
