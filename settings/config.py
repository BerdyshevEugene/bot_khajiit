import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

# токен выдается при регистрации приложения
TOKEN = None
with open('token.txt') as f:
    TOKEN = f.read().strip()
# название БД
NAME_DB = 'products.db'
# версия приложения
VERSION = '0.5.0'
# автор приложния
AUTHOR = 'E.N.'

# родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SHIRTS': emojize('👔 Рубашки'),
    'T-SHIRTS': emojize('👕 Футболки'),
    'PANTS': emojize('👖 Штаны'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('-'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('+'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'SHIRTS': 1,
    'T-SHIRTS': 2,
    'PANTS': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}
