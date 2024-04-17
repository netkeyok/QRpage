import requests


def get_article_name(gs1):
    barcode = gs1[3:16]
    url = f"http://192.168.0.239:8083/v1/get_card?bar={barcode}"
    response = requests.get(url)
    data = response.json()
    if data:
        # Предполагаем, что в ответе всегда будет хотя бы один элемент
        return data[0]['name']
    else:
        return None


if __name__ == '__main__':
    # Пример вызова функции
    barcode = '4640122541638'
    name = get_article_name(barcode)
    print(f" Name: {name}")
