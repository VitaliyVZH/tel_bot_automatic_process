import re
from loguru import logger


def email_address_verification(email: str) -> bool:
    """Функция проверяет email на валидность."""

    logger.info("Проверяем email на валидность")

    pattern_1 = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    pattern_2 = r'(^[\w][\w_.+-]+){1,}@[\w_.-]+\.[\w]{2,}$'

    for pattern in (pattern_1, pattern_2):
        if re.search(pattern, email) is None:
            logger.info("email не валидный")
            return False

    logger.info("email валидный")
    return True
