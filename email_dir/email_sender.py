import os
import smtplib
from loguru import logger
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()


def verify_email_address(sender_email, random_int):
    sender = "jilyaev1987@yandex.ru"
    password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.yandex.ru", 587)

    server.starttls()

    message_body = f'Проверочный код для подтверждения почты {sender_email}: {random_int}'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = sender_email
    msg['Subject'] = 'Подтверждение почты'  # Заголовок письма

    # Добавляем текст сообщения с правильной кодировкой
    msg.attach(MIMEText(message_body, 'plain', 'utf-8'))

    try:
        server.login(sender, password)
        server.sendmail(sender, sender_email, msg.as_string())
        logger.info("Сообщение отправлено на почту")
        return True

    except Exception as _ex:
        logger.warning(f"Сообщение не отправлено\n{_ex}")
        return False


def email_sender(sender_email, message):
    sender = "jilyaev1987@yandex.ru"
    password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.yandex.ru", 587)

    server.starttls()

    message_body = f'{message}'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = sender_email
    msg['Subject'] = 'Данные администратора телеграм бота'  # Заголовок письма

    # Добавляем текст сообщения с правильной кодировкой
    msg.attach(MIMEText(message_body, 'plain', 'utf-8'))

    try:
        server.login(sender, password)
        server.sendmail(sender, sender_email, msg.as_string())
        logger.info("Сообщение отправлено на почту")
        return True

    except Exception as _ex:
        logger.warning(f"Сообщение не отправлено\n{_ex}")
        return False
