import json
from bs4 import BeautifulSoup
from statistics import mean
from collections import Counter


def parse_file(path):
    """
    Парсинг XML-файла и преобразование данных в словарь.
    """
    with open(path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    star = BeautifulSoup(xml_content, features="xml").star
    item = {}

    for el in star:
        if el.name:  # Игнорируем текстовые узлы
            item[el.name] = el.get_text(strip=True)

    # Преобразование числовых полей
    if 'radius' in item:
        item['radius'] = int(item['radius'])
    if 'mass' in item:
        item['mass'] = float(item['mass'])

    return item


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
# Парсинг нескольких файлов
files = ["data/1.xml", "data/2.xml", "data/3.xml"]
data = [parse_file(file) for file in files]

# Сохранение данных в JSON
save_to_json(data, "output.json")

# Сортировка по радиусу
sorted_data = sort_data(data, "radius")
save_to_json(sorted_data, "sorted_by_radius.json")

# Фильтрация по имени звезды
filtered_data = filter_data(data, "name", "Sirius")
save_to_json(filtered_data, "filtered_by_name.json")

# Статистика по радиусу
radius_stats = calculate_statistics(data, "radius")
print("Radius statistics:", radius_stats)

# Частота значений по категории (например, "color")
color_frequency = count_frequency(data, "color")
print("Color frequency:", color_frequency)


