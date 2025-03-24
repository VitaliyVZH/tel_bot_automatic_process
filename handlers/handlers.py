from random import randint

from database.db_manager import Database
from loguru import logger

from email_dir.email_sender import verify_email_address, email_sender
from password_manager import hash_password
from validators.email_validation import email_address_verification

ADMIN_NAME = None
ADMIN_PASSWORD = None
ADMIN_EMAIL = None


def register_role_selection_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["Руководитель", "Администратор", "Подчинённый"])
    def handle_query(call):
        """Отлавливаем нажитие кнопок "Руководитель", "Администратор", "Подчинённый"."""
        logger.info(f"Кнопка нажата: {call.data}, {call.message.chat.id}")
        db = Database()
        if call.data == "Руководитель":
            if db.get_administrator() is False:
                bot.send_message(
                    call.message.chat.id,
                    f"Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора: ")
                bot.register_next_step_handler(call.message, register_administrator_name, bot)
            else:
                bot.answer_callback_query(call.id, "Вы выбрали первую роль!")

        elif call.data == "Администратор":
            if db.get_administrator() is False:
                bot.send_message(
                    call.message.chat.id,
                    "Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора:")
                bot.register_next_step_handler(call.message, register_administrator_name, bot)
            else:
                bot.send_message(call.message.chat.id, "Для работы в роли Администратора необходимо ввести пароль.\n"
                                                   "Введите пароль Администратора:")

        elif call.data == "Подчинённый":
            if db.get_administrator() is False:
                bot.send_message(
                    call.message.chat.id,
                    "Администратор не создан.\nВы первый пользователь.\nВведите данные администратора.\n\n"
                    "Введите имя администратора:")
                bot.register_next_step_handler(call.message, register_administrator_name, bot)
            else:
                bot.answer_callback_query(call.id, "Вы выбрали третью роль!")


def register_administrator_name(call, bot):
    """Получение имени админа."""
    global ADMIN_NAME
    ADMIN_NAME = call.text
    bot.send_message(call.chat.id, f"Имя администратора: <b>{ADMIN_NAME}</b>\n"
                                   f"Введите почту для администратора (нужно подтвердить):", parse_mode="html")
    bot.register_next_step_handler(call, register_administrator_email_1, bot)


def register_administrator_email_1(call, bot):
    """Получение и валидация EMAIL админа."""
    global ADMIN_EMAIL, ADMIN_NAME
    if email_address_verification(call.text):
        bot.send_message(call.chat.id, f"Имя администратора: <b>{ADMIN_NAME}</b>\n"
                                       f"На вашу почту <b>'{call.text}'</b> отправлен проверочный код.\n"
                                       f"Введите код из письма", parse_mode="html")
        ADMIN_EMAIL = call.text
        random_int = randint(1000, 9999)
        verify_email_address(call.text, random_int)
        bot.register_next_step_handler(call, register_administrator_email_2, bot, random_int)
    else:
        bot.send_message(call.chat.id,
                         f"Имя администратора: <b>{ADMIN_NAME}</b>\n"
                         f"Указанная вами почта <b>'{call.text}'</b> не валидна, введите валидную почту:",
                         parse_mode='html')
        bot.register_next_step_handler(call, register_administrator_email_1, bot)


def register_administrator_email_2(call, bot, random_int):
    """Подтверждение EMAIL админа."""
    global ADMIN_EMAIL, ADMIN_NAME
    if str(call.text) == str(random_int):
        logger.info("Проверочный код для подтверждения почты совпал")
        bot.send_message(call.chat.id, "Проверочный код совпал.\n"
                                       "Создайте пароль для администратора:")
        bot.register_next_step_handler(call, register_admin_password, bot)
    else:
        ADMIN_EMAIL = None
        logger.warning("Проверочный код для подтверждения почты не совпал")
        bot.send_message(call.chat.id, f"Проверочный код для подтверждения почты не совпал.\n"
                                       f"Повторно введите адрес электронной почты.", parse_mode="html")
        bot.register_next_step_handler(call, register_administrator_email_1, bot)


def register_admin_password(call, bot):
    """Получение Пароля админа, сохранение данных админа в БД."""
    global ADMIN_EMAIL, ADMIN_NAME
    logger.info(f"Записывается пароль для администратора {call}")
    last_name = call.from_user.last_name
    user_tag = call.from_user.username
    user_id = call.from_user.id
    password = hash_password(call.text)  # Хеширование пароля
    db = Database()
    if db.add_administrator(name=ADMIN_NAME, last_name=last_name, user_tag=user_tag, user_id=user_id, password=password, email=ADMIN_EMAIL):
        logger.info(f"Администратор успешно сохранён")
        email_sender(ADMIN_EMAIL, f"Данные для администратора бота:\n"
                     f"Пароль: {call.text};\n")

        bot.send_message(call.chat.id,
                         "Администратор успешно сохранён.\n"
                         f"Пароль администратора был отправлен на вашу почту <b>{ADMIN_EMAIL}</b>", parse_mode="html")
        ADMIN_EMAIL = None
        ADMIN_NAME = None

