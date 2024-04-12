import requests


def get_article_name(barcode):
    url = f"http://192.168.0.239:8083/v1/get_card?bar={barcode}"
    response = requests.get(url)
    data = response.json()
    print(data)
    if data:
        # Предполагаем, что в ответе всегда будет хотя бы один элемент
        return data[0]['article'], data[0]['name']
    else:
        return None, None


if __name__ == '__main__':
    # Пример вызова функции
    barcode = '4640122541638'
    get_article_name(barcode)
    article, name = get_article_name(barcode)
    print(f"Article: {article}, Name: {name}")
