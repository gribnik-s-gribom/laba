import json
from bs4 import BeautifulSoup
from statistics import mean


def parse_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    clothings = BeautifulSoup(xml_content, features="xml").find_all("clothing")
    items = []

    for clothing in clothings:
        item = {}
        # Обязательные поля
        item["id"] = int(clothing.id.get_text(strip=True)) if clothing.id else None
        item["name"] = clothing.name.get_text(strip=True) if clothing.name else None
        item["category"] = clothing.category.get_text(strip=True) if clothing.category else None
        item["size"] = clothing.size.get_text(strip=True) if clothing.size else None
        item["color"] = clothing.color.get_text(strip=True) if clothing.color else None
        item["material"] = clothing.material.get_text(strip=True) if clothing.material else None
        item["price"] = float(clothing.price.get_text(strip=True)) if clothing.price else None
        item["rating"] = float(clothing.rating.get_text(strip=True)) if clothing.rating else None
        item["reviews"] = int(clothing.reviews.get_text(strip=True)) if clothing.reviews else None

        # Опциональные поля
        item["sporty"] = clothing.sporty.get_text(strip=True) == "yes" if clothing.sporty else None
        item["new"] = clothing.new.get_text(strip=True) == "+" if clothing.new else None
        item["exclusive"] = clothing.exclusive.get_text(strip=True) == "yes" if clothing.exclusive else None

        items.append(item)

    return items


def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def sort_data(data, field):
    return sorted(data, key=lambda x: x.get(field, 0))


def filter_data(data, field, value):
    return [item for item in data if item.get(field) == value]


def calculate_statistics(data, field):
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
    from collections import Counter
    values = [item[field] for item in data if field in item and isinstance(item[field], str)]
    return dict(Counter(values))


# Пример использования
data = parse_file("data/4.xml")

# Сохранение в JSON
save_to_json(data, "output.json")

# Сортировка по цене
sorted_data = sort_data(data, "price")
save_to_json(sorted_data, "sorted_by_price.json")

# Фильтрация по категории
filtered_data = filter_data(data, "category", "casual")
save_to_json(filtered_data, "filtered_by_category.json")

# Статистика по рейтингу
rating_stats = calculate_statistics(data, "rating")
print("Rating statistics:", rating_stats)

# Частота значений по цвету
color_frequency = count_frequency(data, "color")
print("Color frequency:", color_frequency)
