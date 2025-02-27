from abc import ABC, abstractmethod


# Абстрактный класс для продукта
class Product(ABC):
    @abstractmethod
    def display_info(self):
        pass


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
    def __init__(self, date, time, weight, diameter, shape, color, flavor):
        self.date = date
        self.time = time
        self.weight = weight
        self.diameter = diameter
        self.shape = shape
        self.color = color
        self.flavor = flavor

    def display_info(self):
        return (f"Информация о заказе: Дата: {self.date}, Время: {self.time}, "
                f"Вес: {self.weight} кг, Диаметр: {self.diameter} см, "
                f"Форма: {self.shape}, Цвет: {self.color}, Вкус: {self.flavor}")

    def update_weight(self, new_weight):
        if new_weight < 0:
            raise ValueError("Вес не может быть отрицательным.")
        self.weight = new_weight

    def update_diameter(self, new_diameter):
        if new_diameter < 0:
            raise ValueError("Диаметр не может быть отрицательным.")
        self.diameter = new_diameter

    def update_shape(self, new_shape):
        self.shape = new_shape

    def update_color(self, new_color):
        self.color = new_color

    def update_flavor(self, new_flavor):
        self.flavor = new_flavor

    def update_order(self, date=None, time=None, weight=None, diameter=None,
                     shape=None, color=None, flavor=None):
        if date:
            self.date = date
        if time:
            self.time = time
        if weight is not None:
            self.update_weight(weight)
        if diameter is not None:
            self.update_diameter(diameter)
        if shape:
            self.shape = shape
        if color:
            self.color = color
        if flavor:
            self.flavor = flavor

    def __add__(self, other):
        if not isinstance(other, Order):
            raise ValueError("Сложение возможно только с другим объектом Order")

        combined_weight = self.weight + other.weight
        combined_diameter = (self.diameter + other.diameter) / 2

        return Order(
            date=self.date,
            time=self.time,
            weight=combined_weight,
            diameter=combined_diameter,
            shape=self.shape,
            color=self.color,
            flavor=self.flavor
        )

    def __sub__(self, other):
        if not isinstance(other, Order):
            raise ValueError("Вычитание возможно только с другим объектом Order")

        weight_difference = self.weight - other.weight

        return Order(
            date=self.date,
            time=self.time,
            weight=weight_difference,
            diameter=self.diameter,
            shape=self.shape,
            color=self.color,
            flavor=self.flavor
        )

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False

        return (
                self.date == other.date and
                self.time == other.time and
                self.weight == other.weight and
                self.diameter == other.diameter and
                self.shape == other.shape and
                self.color == other.color and
                self.flavor == other.flavor
        )


class Catalog(Product):  # Наследуем от абстрактного класса Product
    def __init__(self, name, image_url, ingredients):
        super().__init__()
        self.name = name
        self.image_url = image_url
        self.ingredients = ingredients

    def display_info(self):  # Реализация абстрактного метода
        return (f"Торт: {self.name}, Фото: {self.image_url}, "
                f"Ингредиенты: {', '.join(self.ingredients)}")


class Booking:
    def __init__(self, available_times):
        self.available_times = available_times

    def book(self, client, order):
        if order.time in self.available_times:
            self.available_times.remove(order.time)
            return True
        return False


# Создание иерархии пользовательских исключений
class BaseApplicationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ClientError(BaseApplicationError):
    def __init__(self, message):
        super().__init__(message)


class OrderError(BaseApplicationError):
    def __init__(self, message):
        super().__init__(message)


class InvalidOrderTimeError(OrderError):
    def __init__(self, message):
        super().__init__(message)


class InvalidOrderFlavorError(OrderError):
    def __init__(self, message):
        super().__init__(message)


class InvalidClientDataError(ClientError):
    def __init__(self, message):
        super().__init__(message)


def main():
    clients = []

    catalog = [
        Catalog("Шоколадный торт", "url_to_image1", ["мука", "сахар", "какао", "яйца"]),
        Catalog("Торт Сникерс", "url_to_image2", ["мука", "сахар", "карамель", "арахис"]),
    ]

    booking = Booking(["10:00", "11:00", "12:00", "13:00", "14:00"])

    print("Добавление клиентов и заказов.")

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
                weight = float(input("Введите вес торта (кг): "))
            except ValueError:
                raise OrderError("Некорректный вес торта.")

            try:
                diameter = float(input("Введите диаметр торта (см): "))
            except ValueError:
                raise OrderError("Некорректный диаметр торта.")

            shape = input("Введите форму торта (круг, квадрат, сердце): ")

            color = input("Введите цвет торта: ")

            print("\nДоступные вкусы тортов:")

            for index, item in enumerate(catalog):
                print(f"{index + 1}. {item.display_info()}")

            try:
                flavor_choice = int(input("Выберите вкус торта (введите номер): ")) - 1
            except ValueError:
                raise OrderError("Некорректный выбор вкуса.")

            if 0 <= flavor_choice < len(catalog):
                flavor_catalog_item = catalog[flavor_choice]
                order = Order(date, time, weight, diameter, shape, color, flavor_catalog_item)

                client.add_order(order)

                if booking.book(client, order):
                    print(f"Заказ для клиента {client.name} успешно забронирован на время {time}.")
                    print(order.display_info())

                    # Демонстрация перегруженных операторов.
                    if len(client.orders) > 1:
                        combined_order = client.orders[-1] + client.orders[-2]
                        print("\nОбъединенный заказ:")
                        print(combined_order.display_info())

                        difference_order = client.orders[-1] - client.orders[-2]
                        print("\nЗаказ с вычитанием веса:")
                        print(difference_order.display_info())

                        is_equal = client.orders[-1] == client.orders[-2]
                        print(f"\nЗаказы равны по ID? {'Да' if is_equal else 'Нет'}")

                else:
                    raise InvalidOrderTimeError("Не удалось забронировать время для клиента.")

            else:
                raise InvalidOrderFlavorError("Неверный выбор вкуса.")

        except InvalidClientDataError as e:
            print(f"Ошибка клиента: {e}")
        except InvalidOrderTimeError as e:
            print(f"Ошибка времени заказа: {e}")
        except InvalidOrderFlavorError as e:
            print(f"Ошибка выбора вкуса: {e}")
        except OrderError as e:
            print(f"Общая ошибка заказа: {e}")
        except Exception as e:
            print(f"Произошла общая ошибка: {e}")
        finally:
            # Код, который выполняется всегда
            print(f"Обработка клиента #{client_id} завершена.")
            print(f"Всего клиентов: {Client.get_total_clients()}")

        client_id += 1

        another_client = input("\nХотите добавить еще одного клиента? (да/нет): ").strip().lower()
        if another_client != 'да':
            break

    print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()
