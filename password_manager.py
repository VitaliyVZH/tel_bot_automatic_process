from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Создаем экземпляр PasswordHasher
ph = PasswordHasher()


def hash_password(password):
    """Хеширование пароля."""
    return ph.hash(password)


def check_password(hashed_password, user_password):
    """Функция для проверки пароля."""
    try:
        # Проверяем, совпадает ли введенный пароль с хешем
        ph.verify(hashed_password, user_password)
        return True
    except VerifyMismatchError:
        return False
