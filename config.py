# config.py

class Config:
    """Основная конфигурация приложения"""
    LOGGING_ENABLED = True  # Включение/выключение логирования
    LOG_FILE = 'www.log'   # Имя файла лога
    LOG_LEVEL = 'DEBUG'    # Уровень логирования (DEBUG, INFO, ERROR и т.д.)
    MAX_LOG_SIZE = 10**6   # Максимальный размер файла лога в байтах
    BACKUP_COUNT = 3       # Количество архивных логов