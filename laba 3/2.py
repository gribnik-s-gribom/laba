import json
from bs4 import BeautifulSoup
from statistics import mean
from collections import Counter
import re

def parse_html_file(path):
    """
    Парсинг HTML-файла и извлечение данных о продуктах.
    """
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("div", class_="product-item")
    items = []

    for product in products:
        item = {}

        # Извлечение ID продукта
        favorite_link = product.find("a", class_="add-to-favorite")
        if favorite_link and "data-id" in favorite_link.attrs:
            item["id"] = int(favorite_link["data-id"])

        # Извлечение названия
        name_span = product.find("span")
        if name_span:
            item["name"] = name_span.get_text(strip=True)

        # Извлечение цены
        price_tag = product.find("price")
        if price_tag:
            price_text = price_tag.get_text(strip=True).replace("₽", "").replace(" ", "")
            item["price"] = int(price_text)

        # Извлечение бонусов
        bonus_strong = product.find("strong")
        if bonus_strong:
            bonus_text = re.search(r"\d+", bonus_strong.get_text(strip=True))
            if bonus_text:
                item["bonus"] = int(bonus_text.group())

        # Извлечение характеристик
        ul = product.find("ul")
        if ul:
            for li in ul.find_all("li"):
                li_type = li.get("type")
                if li_type:
                    item[li_type] = li.get_text(strip=True)

        items.append(item)

    return items

def save_to_json(data, output_path):
    """
    Сохранение данных в JSON-файл.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def sort_data(data, field):
    """
    Сортировка списка объектов по указанному полю.
    """
    return sorted(data, key=lambda x: x.get(field, 0))

def filter_data(data, field, value):
    """
    Фильтрация данных по указанному значению поля.
    """
    return [item for item in data if item.get(field) == value]

def calculate_statistics(data, field):
    """
    Вычисление статистических характеристик для числового поля.
    """
    values = [item[field] for item in data if field in item and isinstance(item[field], (int, float))]
    if not values:
        return {}
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values)
    }

def count_frequency(data, field):
    """
    Подсчет частоты значений для текстового поля.
    """
    values = [item[field] for item in data if field in item]
    return dict(Counter(values))

# Пример использования
files = ["data/1.html", "data/2.html", "data/3.html"]
data = []
for file in files:
    data.extend(parse_html_file(file))

# Сохранение данных в JSON
save_to_json(data, "output.json")

# Сортировка по цене
sorted_data = sort_data(data, "price")
save_to_json(sorted_data, "sorted_by_price.json")

# Фильтрация по разрешению экрана
filtered_data = filter_data(data, "resolution", "1920x2160")
save_to_json(filtered_data, "filtered_by_resolution.json")

# Статистика по цене
price_stats = calculate_statistics(data, "price")
print("Price statistics:", price_stats)

# Частота значений по типу экрана (матрице)
matrix_frequency = count_frequency(data, "matrix")
print("Matrix frequency:", matrix_frequency)
