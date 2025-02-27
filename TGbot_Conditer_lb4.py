from abc import ABC, abstractmethod

class BaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidOrderError(BaseError):
    def __init__(self, message):
        super().__init__(message)

class InvalidClientDataError(BaseError):
    def __init__(self, message):
        super().__init__(message)


class Product(ABC):
    @abstractmethod
    def display_info(self):
        pass


class ProductItem(Product):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_info(self):
        return f"Товар: {self.name}, Цена: {self.price} руб."


class Client:
    total_clients = 0

    def __init__(self, client_id, name, phone_number, address):
        self.client_id = client_id
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.orders = []

        Client.total_clients += 1

    @staticmethod
    def from_input(client_id):
        print(f"\nВведите данные для клиента #{client_id}:")
        name = input("Введите полное имя клиента: ")
        phone_number = input("Введите номер телефона клиента: ")
        address = input("Введите адрес клиента: ")
        return Client(client_id, name, phone_number, address)

    @classmethod
    def get_total_clients(cls):
        return cls.total_clients

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"Клиент ID: {self.client_id}, Имя: {self.name}, Телефон: {self.phone_number}, Адрес: {self.address}"

    def __repr__(self):
        return f"Client({self.client_id}, '{self.name}', '{self.phone_number}', '{self.address}')"


class Order:
    def __init__(self, date, time, weight, diameter, color, shape, product_name):
        self._date = date
        self._time = time
        self._weight = weight
        self._diameter = diameter
        self._color = color
        self._shape = shape
        self.product_name = product_name

    def display_info(self):
        return (f"Информация о заказе: Дата: {self._date}, Время: {self._time}, "
                f"Вес: {self._weight} кг, Диаметр: {self._diameter} см, "
                f"Цвет: {self._color}, Форма: {self._shape}, Товар: {self.product_name}")

    def get_date(self):
        return self._date

    def get_time(self):
        return self._time

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"Order('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}')"


class SpecialOrder(Order):
    def __init__(self, date, time, weight, diameter, color, shape, product_name, special_request):
        super().__init__(date, time, weight, diameter, color, shape, product_name)
        self.special_request = special_request

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Специальная просьба: {self.special_request}"

    def process_order_info(self, priority="special"):
        if priority == "special":
            print("Приоритет специального заказа:")
            print(self.display_info())
            super().display_info()
        else:
            print("Приоритет базового заказа:")
            super().display_info()
            print(self.display_info())

    def __str__(self):
        return self.display_info()

    def __repr__(self):
        return f"SpecialOrder('{self._date}', '{self._time}', {self._weight}, {self._diameter}, '{self._color}', '{self._shape}', '{self.product_name}', '{self.special_request}')"


class Booking:
    def __init__(self, available_times):
        self.available_times = available_times

    def book(self, client, order):
        if order.get_time() in self.available_times:
            self.available_times.remove(order.get_time())
            return True
        return False


def create_product_list():
    product_list = [
        ProductItem("Торт Шоколадный", 500),
        ProductItem("Торт ванильный", 480),
        ProductItem("Сложный декор", 200)
    ]

    print("Список доступных товаров:")
    for index, item in enumerate(product_list):
        print(f"{index + 1}. {item.display_info()}")
    print()

    return product_list


def find_max_attribute_item(two_dim_list, attribute_name):
    if not two_dim_list:
        return None

    max_item = None
    max_value = float('-inf')

    for row in two_dim_list:
        for item in row:
            attribute_value = getattr(item, attribute_name, None)
            if attribute_value is not None and attribute_value > max_value:
                max_value = attribute_value
                max_item = item

    return max_item


def main():
    product_list = create_product_list()

    two_dim_list = [
        [
            ProductItem("Торт", 500),
            ProductItem("Пирожное", 100),
            ProductItem("Капкейк", 50)
        ],
        [
            ProductItem("Маффин", 200),
            ProductItem("Булочка", 150),
            ProductItem("Печенье", 75)
        ]
    ]

    max_price_item = find_max_attribute_item(two_dim_list, 'price')
    if max_price_item:
        print(f"\nТовар с максимальной ценой: {max_price_item.display_info()}")
    else:
        print("\nСписок пуст или атрибут не найден.")

    clients = []
    booking = Booking(["10:00", "11:00", "12:00", "13:00", "14:00"])

    print("Добавление клиентов и заказов")

    client_id = 1

    while True:
        try:
            client = Client.from_input(client_id)
            if not client.name or not client.phone_number or not client.address:
                raise InvalidClientDataError("Некорректные данные клиента.")
            clients.append(client)

            print("\nСоздаем заказ для клиента:")

            date = input("Введите дату заказа (гггг-мм-дд): ")
            time = input("Введите время заказа (чч:мм): ")

            try:
                weight = float(input("Введите вес товара (кг): "))
            except ValueError:
                raise InvalidOrderError("Некорректный вес товара.")

            try:
                diameter = float(input("Введите диаметр товара (см): "))
            except ValueError:
                raise InvalidOrderError("Некорректный диаметр товара.")

            color = input("Введите цвет товара: ")

            print("\nВыберите форму торта:")
            print("1. Круг")
            print("2. Квадрат")
            print("3. Сердце")
            try:
                shape_choice = int(input("Введите номер формы: "))
            except ValueError:
                raise InvalidOrderError("Некорректный выбор формы.")

            if shape_choice == 1:
                shape = "круг"
            elif shape_choice == 2:
                shape = "квадрат"
            elif shape_choice == 3:
                shape = "сердце"
            else:
                raise InvalidOrderError("Неверный выбор формы.")

            print("\nВыберите товар:")
            for index, item in enumerate(product_list):
                print(f"{index + 1}. {item.display_info()}")

            try:
                product_choice = int(input("Введите номер товара: ")) - 1
            except ValueError:
                raise InvalidOrderError("Некорректный выбор товара.")

            if 0 <= product_choice < len(product_list):
                product_name = product_list[product_choice].name
                special_request = input("Введите специальную просьбу (если есть): ")

                if special_request:
                    order = SpecialOrder(date, time, weight, diameter, color, shape, product_name, special_request)
                else:
                    order = Order(date, time, weight, diameter, color, shape, product_name)

                client.add_order(order)

                if booking.book(client, order):
                    print(f"Заказ для клиента {client.name} успешно забронирован на время {time}.")
                    print(order.display_info())

                else:
                    raise InvalidOrderError("Не удалось забронировать время для клиента.")

            else:
                raise InvalidOrderError("Неверный выбор товара.")

        except InvalidClientDataError as e:
            print(f"Ошибка клиента: {e}")
        except InvalidOrderError as e:
            print(f"Ошибка заказа: {e}")
        except Exception as e:
            print(f"Произошла общая ошибка: {e}")
        finally:
            print(f"Обработка клиента #{client_id} завершена.")
            print(f"Всего клиентов: {Client.get_total_clients()}")

        client_id += 1

        another_client = input("\nХотите добавить еще одного клиента? (да/нет): ").strip().lower()
        if another_client != 'да':
            break

    print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()
