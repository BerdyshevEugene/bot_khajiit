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
        обрабатывает входящие текстовые сообщения
        при нажатии на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, 'Вы вернулись назад',
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'.
        Выбор товара из категории
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(
                                  config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_order(self, message):
        """
        обрабатывает входящие текстовые
        сообщения при нажатии на кнопку 'Заказ'
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(
            message.chat.id,
            MESSAGES['order'].
            format(self.BD.select_single_product_name(product_id),
                   self.BD.select_single_product_title(product_id),
                   self.BD.select_single_product_price(product_id),
                   self.BD.select_order_quantity(product_id)),
            parse_mode="HTML",
            reply_markup=self.keyboards.orders_menu(self.step, quantity)
        )

    def pressed_btn_up(self, message):
        """
        Обрабатывает входящие текстовые сообщения при нажатии
        на кнопку up.
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции на складе
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД orders
            self.BD.update_order_value(
                count[self.step], 'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(
                count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        """
        Обрабатывает входящие текстовые сообщения при нажатии
        на кнопку down.
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции на складе
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар в заказе есть
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД orders
            self.BD.update_order_value(
                count[self.step], 'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(
                count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обрабатывает входящие текстовые сообщения при нажатии
        на кнопку X.
        """
        # получаем список всех product_id заказа
        count = self.BD.select_all_product_id()
        # если список не пустой
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # получаем количество товара к конкретной позиции
            # заказа для возврата на склад (в product)
            quantity_product = self.BD.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.BD.delete_order(count[self.step])
            # вносим изменения в БД product
            self.BD.update_product_value(
                count[self.step], 'quantity', quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # если товара в заказе нет, отправляем следующее сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keyboards.category_menu())

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

            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        MESSAGES['no_orders'],
                        parse_mode='HTML',
                        reply_markup=self.keyboards.category_menu()
                    )

            # ********** меню (по категориям товаров) ********** #
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # ********** меню (Заказа) ********** #
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)
