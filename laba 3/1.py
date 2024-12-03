import json
from bs4 import BeautifulSoup
from statistics import mean
from collections import Counter

def parse_html_file(path):
    """
    Парсинг HTML-файла и извлечение данных.
    """
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, features="html.parser")
    build = soup.find("div", attrs={"class": "chess-wrapper"})
    if not build:
        return None

    item = {}
    # Извлечение типа
    type_span = build.find("span", text=lambda t: "Тип:" in t)
    if type_span:
        item["type"] = type_span.get_text(strip=True).replace("Тип:", "").strip()

    # Извлечение заголовка и идентификатора
    title_h1 = build.find("h1", class_="title")
    if title_h1:
        item["tournament"] = title_h1.get_text(strip=True).replace("Турнир:", "").strip()
        item["id"] = int(title_h1.get("id"))

    # Извлечение города и начала
    address_p = build.find("p", class_="address-p")
    if address_p:
        item["city"] = address_p.get_text(strip=True).split("Город:")[1].split("Начало:")[0].strip()
        item["start_date"] = address_p.get_text(strip=True).split("Начало:")[1].strip()

    # Извлечение информации
    info_div = build.find("div", text=lambda t: "Информация:" in t)
    if info_div:
        count_span = build.find("span", class_="count")
        year_span = build.find("span", class_="year")
        rating_span = build.find("span", text=lambda t: "Минимальный рейтинг" in t)
        if count_span:
            item["rounds"] = int(count_span.get_text(strip=True).replace("Количество туров:", "").strip())
        if year_span:
            item["time_control"] = year_span.get_text(strip=True).replace("Контроль времени:", "").strip()
        if rating_span:
            item["min_rating"] = int(rating_span.get_text(strip=True).replace("Минимальный рейтинг для участия:", "").strip())

    # Извлечение рейтинга и просмотров
    stats_div = build.find_all("span")
    for stat in stats_div:
        if "Рейтинг:" in stat.get_text():
            item["rating"] = float(stat.get_text(strip=True).replace("Рейтинг:", "").strip())
        if "Просмотры:" in stat.get_text():
            item["views"] = int(stat.get_text(strip=True).replace("Просмотры:", "").strip())

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
files = ["data/1.html", "data/2.html", "data/3.html"]
data = [parse_html_file(file) for file in files if parse_html_file(file)]

# Сохранение данных в JSON
save_to_json(data, "output.json")

# Сортировка по просмотрам
sorted_data = sort_data(data, "views")
save_to_json(sorted_data, "sorted_by_views.json")

# Фильтрация по городу
filtered_data = filter_data(data, "city", "Алма-Ата")
save_to_json(filtered_data, "filtered_by_city.json")

# Статистика по просмотрам
views_stats = calculate_statistics(data, "views")
print("Views statistics:", views_stats)

# Частота значений по типу
type_frequency = count_frequency(data, "type")
print("Type frequency:", type_frequency)


