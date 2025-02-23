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


class Order(Product):  # Наследуем от абстрактного класса Product
    order_counter = 1

    def __init__(self, date, time, weight, diameter, shape, color, flavor):
        super().__init__()
        self.order_id = Order.order_counter
        Order.order_counter += 1
        self.date = date
        self.time = time
        self.weight = weight
        self.diameter = diameter
        self.shape = shape
        self.color = color
        self.flavor = flavor

    def display_info(self):  # Реализация абстрактного метода
        return (f"Заказ ID: {self.order_id}, Дата: {self.date}, Время: {self.time}, "
                f"Вес: {self.weight} кг, Диаметр: {self.diameter} см, "
                f"Форма: {self.shape}, Цвет: {self.color}, Вкус: {self.flavor.name}")

    # Перегрузка оператора
    def __add__(self, other):
        if isinstance(other, Order):
            combined_weight = self.weight + other.weight
            return Order(
                date=self.date,
                time=self.time,
                weight=combined_weight,
                diameter=self.diameter,
                shape=self.shape,
                color=self.color,
                flavor=self.flavor
            )
        return NotImplemented

    # Перегрузка оператора
    def __sub__(self, other):
        if isinstance(other, Order):
            return Order(
                date=self.date,
                time=self.time,
                weight=max(0, self.weight - other.weight),  # Не допускаем отрицательный вес
                diameter=self.diameter,
                shape=self.shape,
                color=self.color,
                flavor=self.flavor
            )
        return NotImplemented

    # Перегрузка оператора
    def __eq__(self, other):
        if isinstance(other, Order):
            return self.order_id == other.order_id
        return NotImplemented


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
        client = Client.from_input(client_id)
        clients.append(client)

        print("\nСоздаем заказ для клиента:")

        date = input("Введите дату заказа (гггг-мм-дд): ")

        time = input("Введите время заказа (чч:мм): ")

        weight = float(input("Введите вес торта (кг): "))

        diameter = float(input("Введите диаметр торта (см): "))

        shape = input("Введите форму торта (круг, квадрат, сердце): ")

        color = input("Введите цвет торта: ")

        print("\nДоступные вкусы тортов:")


        for index, item in enumerate(catalog):
            print(f"{index + 1}. {item.display_info()}")

        flavor_choice = int(input("Выберите вкус торта (введите номер): ")) - 1

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
                print(f"Не удалось забронировать время для клиента {client.name}.")

        else:
            print("Неверный выбор вкуса. Заказ не создан.")

        client_id += 1

        another_client = input("\nХотите добавить еще одного клиента? (да/нет): ").strip().lower()
        if another_client != 'да':
            break


print(f"\nОбщее количество клиентов: {Client.get_total_clients()}")


if __name__ == "__main__":
    main()
