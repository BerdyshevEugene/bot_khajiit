# импортируем ответ пользователю
from settings.message import MESSAGES
from settings import config
# импортируем класс-родитель
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения при нажатии на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        """
        обрабатывает входящие текстовые сообщения
        при нажатии на кнопку 'Выбрать товар'
        """
        self.bot.send_message(message.chat.id, 'Каталог категорий товара',
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, 'Сделайте свой выбор',
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_info(self, message):
        """
        обрабатывает входящие текстовые сообщения
        при нажатии на кнопку 'О магазине'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        """
        обрабатывает входящие текстовые сообщения
        при нажатии на кнопку 'Настройки'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        """
        обрабатывает входящие текстовые сообщения при нажатии на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keyboards.start_menu())

    def handle(self):
        # обработчик(декоратор) сообщений, который обрабатывает
        # входящие текстовые сообщения при нажатии кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** меню ********** #

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)
