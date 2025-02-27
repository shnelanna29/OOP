class ProductItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_info(self):
        return f"Товар: {self.name}, Цена: {self.price} руб."


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


# Двумерный список
def create_two_dimensional_list():
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

    print("Двумерный список:")
    for row in two_dim_list:
        for item in row:
            print(item.display_info())
        print()  # Пустая строка для разделения рядов

    max_price_item = find_max_attribute_item(two_dim_list, 'price')
    if max_price_item:
        print(f"\nТовар с максимальной ценой: {max_price_item.display_info()}")
    else:
        print("\nСписок пуст или атрибут не найден.")


# Основная функция
def main():
    create_two_dimensional_list()


if __name__ == "__main__":
    main()
