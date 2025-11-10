import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LevelBasedFormatter(logging.Formatter):
    def __init__(self, default_fmt: str, info_fmt: str, datefmt: str | None = None) -> None:
        super().__init__(datefmt=datefmt)
        self.default_fmt: logging.Formatter = logging.Formatter(default_fmt, datefmt)
        self.info_fmt: logging.Formatter = logging.Formatter(info_fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.INFO:
            return self.info_fmt.format(record)
        return self.default_fmt.format(record)


def kitty_logger(name: str, log_file: str = "kitty.log", log_level: str = "INFO") -> logging.Logger:
    """
    Sets up a logger with console and rotating file handlers.

    Args:
        name (str): Name of the logger (usually __name__ of the calling module).
        log_file (str): Path to the log file. Defaults to 'kitty.log'.
        log_level (str): Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'). Defaults to 'INFO'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if not logger.handlers:
        default_fmt = "PurrfectKit | %(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
        info_fmt = "PurrfectKit | %(asctime)s [%(levelname)s] - %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"

        formatter = LevelBasedFormatter(default_fmt, info_fmt, datefmt)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_dir = Path(".cache/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / log_file

        file_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
