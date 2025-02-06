import logging
import colorlog

logger = logging.getLogger('pig_logger')
logger.setLevel(logging.DEBUG)

# log format
formatter = colorlog.ColoredFormatter(
    "%(asctime)s | %(log_color)s%(levelname)s%(reset)s | %(blue)s%(filename)s:%(lineno)s%(reset)s | %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# log to file and console
file_handler = logging.FileHandler('pig.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
