from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def display_info(self):
        pass


class ProductItem:
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


class Order:
    def __init__(self, date, time, weight, product_name):
        self.date = date
        self.time = time
        self.weight = weight
        self.product_name = product_name

    def display_info(self):
        return f"Информация о заказе: Дата: {self.date}, Время: {self.time}, Вес: {self.weight} кг, Товар: {self.product_name}"


class SpecialOrder(Order):
    def __init__(self, date, time, weight, product_name, special_request):
        super().__init__(date, time, weight, product_name)
        self.special_request = special_request

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Специальная просьба: {self.special_request}"


class Booking:
    def __init__(self, available_times):
        self.available_times = available_times

    def book(self, client, order):
        if order.time in self.available_times:
            self.available_times.remove(order.time)
            return True
        return False


class InvalidOrderError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidClientDataError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def create_product_list():
    product_list = [
        {"name": "Торт Шоколадный", "price": 500},
        {"name": "Торт ванильный", "price": 480},
        {"name": "Сложный декор", "price": 200}
    ]

    print("Список доступных товаров:")
    for index, item in enumerate(product_list):
        print(f"{index + 1}. {item['name']}: {item['price']} руб/кг")
    print()

    return product_list


# Основная функция
def main():
    product_list = create_product_list()

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

            print("\nВыберите товар:")
            for index, item in enumerate(product_list):
                print(f"{index + 1}. {item['name']}")

            try:
                product_choice = int(input("Введите номер товара: ")) - 1
            except ValueError:
                raise InvalidOrderError("Некорректный выбор товара.")

            if 0 <= product_choice < len(product_list):
                product_name = product_list[product_choice]['name']
                special_request = input("Введите специальную просьбу (если есть): ")

                if special_request:
                    order = SpecialOrder(date, time, weight, product_name, special_request)
                else:
                    order = Order(date, time, weight, product_name)

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
