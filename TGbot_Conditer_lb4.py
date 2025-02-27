from abc import ABC, abstractmethod

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


class BaseOrder:
    def __init__(self, date, time, weight, diameter, shape, color, flavor):
        self.date = date
        self.time = time
        self._weight = weight  
        self._diameter = diameter  
        self.shape = shape
        self.color = color
        self.flavor = flavor

    def display_info(self):
        return (f"Информация о заказе: Дата: {self.date}, Время: {self.time}, "
                f"Вес: {self._weight} кг, Диаметр: {self._diameter} см, "
                f"Форма: {self.shape}, Цвет: {self.color}, Вкус: {self.flavor}")

    def update_weight(self, new_weight):
        if new_weight < 0:
            raise ValueError("Вес не может быть отрицательным.")
        self._weight = new_weight

    def update_diameter(self, new_diameter):
        if new_diameter < 0:
            raise ValueError("Диаметр не может быть отрицательным.")
        self._diameter = new_diameter

    def print_base_info(self):
        print("Это базовый заказ")



class SpecialOrder(BaseOrder):
    def __init__(self, date, time, weight, diameter, shape, color, flavor, special_request):
        # Вызов конструктора базового класса через super()
        super().__init__(date, time, weight, diameter, shape, color, flavor)
        self.special_request = special_request

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Специальная просьба: {self.special_request}"

    def add_special_decoration(self, decoration):
        self.special_request += f", Дополнительная декорация: {decoration}"

    def print_special_info(self):
        super().print_base_info()  
        print(f"Специальная просьба: {self.special_request}")

    def access_protected_attributes(self):
        # Доступ к защищенным атрибутам в производном классе
        print(f"Вес: {self._weight} кг")
        print(f"Диаметр: {self._diameter} см")


class Catalog(Product):  
    def __init__(self, name, image_url, ingredients):
        super().__init__()
        self.name = name
        self.image_url = image_url
        self.ingredients = ingredients

    def display_info(self): 
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

class InvalidOrderError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidClientDataError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
                raise InvalidOrderError("Некорректный вес торта.")

            try:
                diameter = float(input("Введите диаметр торта (см): "))
            except ValueError:
                raise InvalidOrderError("Некорректный диаметр торта.")

            shape = input("Введите форму торта (круг, квадрат, сердце): ")

            color = input("Введите цвет торта: ")

            print("\nДоступные вкусы тортов:")

            for index, item in enumerate(catalog):
                print(f"{index + 1}. {item.display_info()}")

            try:
                flavor_choice = int(input("Выберите вкус торта (введите номер): ")) - 1
            except ValueError:
                raise InvalidOrderError("Некорректный выбор вкуса.")

            if 0 <= flavor_choice < len(catalog):
                flavor_catalog_item = catalog[flavor_choice]
                special_request = input("Введите специальную просьбу (если есть): ")

                if special_request:
                    order = SpecialOrder(date, time, weight, diameter, shape, color, flavor_catalog_item, special_request)
                else:
                    order = BaseOrder(date, time, weight, diameter, shape, color, flavor_catalog_item)

                client.add_order(order)

                if booking.book(client, order):
                    print(f"Заказ для клиента {client.name} успешно забронирован на время {time}.")
                    print(order.display_info())

                    if isinstance(order, SpecialOrder):
                        order.access_protected_attributes()  

                else:
                    raise InvalidOrderError("Не удалось забронировать время для клиента.")

            else:
                raise InvalidOrderError("Неверный выбор вкуса.")

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
