from database.db_manager import Database
from loguru import logger

from validators.email_validation import email_address_verification

# Состояния
WAITING_FOR_NAME = 'waiting_for_name'
WAITING_FOR_LAST_NAME = 'waiting_for_last_name'
WAITING_FOR_PASSWORD = 'waiting_for_password'
WAITING_FOR_EMAIL = 'waiting_for_email'


user_states = {}  # Словарь для хранения состояний пользователей


def register_role_selection_handlers(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        logger.info(f"Кнопка нажата: {call.data}")
        # Создаем экземпляр класса Database
        db = Database()

        # Обработка нажатия на кнопку
        if call.data == "Руководитель":
            if db.get_administrator() is False:
                user_states[call.message.chat.id] = WAITING_FOR_NAME
                bot.send_message(
                    call.message.chat.id,
                    "Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора:")
            else:
                bot.answer_callback_query(call.id, "Вы выбрали первую роль!")

        elif call.data == "Администратор":
            if db.get_administrator() is False:
                user_states[call.message.chat.id] = WAITING_FOR_NAME
                bot.send_message(
                    call.message.chat.id,
                    "Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора:")
            else:
                bot.answer_callback_query(call.id, "Вы выбрали вторую роль!")

        elif call.data == "Подчинённый":
            if db.get_administrator() is False:
                user_states[call.message.chat.id] = WAITING_FOR_NAME
                bot.send_message(
                    call.message.chat.id,
                    "Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора:")
            else:
                bot.answer_callback_query(call.id, "Вы выбрали третью роль!")


def register_admin_creation_handler(bot):
    """Получение данных администратора"""
    @bot.message_handler(func=lambda message: message.chat.id in user_states)
    def handle_user_input(message):
        state = user_states[message.chat.id]
        logger.info(f"handle_user_input")

        if state == WAITING_FOR_NAME:
            user_states[str(message.chat.id) + "_name"] = message.text  # Сохраняем имя
            user_states[message.chat.id] = WAITING_FOR_LAST_NAME  # Обновляем состояние
            bot.send_message(message.chat.id, "Фамилия администратора:")

        elif state == WAITING_FOR_LAST_NAME:
            user_states[str(message.chat.id) + "_last_name"] = message.text  # Сохраняем фамилию
            user_states[message.chat.id] = WAITING_FOR_EMAIL  # Обновляем состояние
            bot.send_message(message.chat.id, "Email администратора (нужно подтвердить):")

        elif state == WAITING_FOR_EMAIL:
            if email_address_verification(message.text):
                user_states[str(message.chat.id) + "_email"] = message.text  # Сохраняем почту
                user_states[message.chat.id] = WAITING_FOR_PASSWORD  # Обновляем состояние
                bot.send_message(message.chat.id, "Пароль администратора:")
            else:
                bot.send_message(message.chat.id, "Введённый email невалиден, повторите ввод:")

        elif state == WAITING_FOR_PASSWORD:
            name = user_states[str(message.chat.id) + "_name"]  # Получаем имя из правильного ключа
            last_name = user_states[str(message.chat.id) + "_last_name"]  # Получаем фамилию
            email = user_states[str(message.chat.id) + "_email"]  # Получаем почту
            password = message.text  # Сохраняем пароль

            # Сохраняем данные в БД
            db = Database()
            # Здесь предполагается, что у вас есть метод для добавления администратора
            db.add_administrator(
                name=name, last_name=last_name, user_tag=message.from_user.username, user_id=message.from_user.id,
                password=password, email=email
            )

            bot.send_message(message.chat.id, "Администратор успешно создан!")
            del user_states[message.chat.id]  # Удаляем состояние пользователя
