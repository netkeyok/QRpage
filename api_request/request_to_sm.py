import requests


def get_article_name(gs1):
    barcode = gs1[3:16]
    url = f"http://192.168.0.239:8083/v1/get_card?bar={barcode}"
    response = requests.get(url)
    # print(response)
    data = response.json()
    if data:
        # Предполагаем, что в ответе всегда будет хотя бы один элемент
        # print(data)
        return data['name']
    else:
        return None


if __name__ == '__main__':
    # Пример вызова функции
    barcode = '0104680089950555215trj5Ij936FG8'
    # barcode = '0104680089950661215N3fCGj93yMdb'
    name = get_article_name(barcode)
    print(f" Name: {name}")
