# import requests
# import json
# import pandas as pd
# import concurrent.futures
# from threading import Lock
# from urllib.parse import quote
#
# with open('keys_test.txt', 'r', encoding='utf-8') as f:
#     keywords = [line.strip() for line in f]
#
# lock = Lock()
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Origin': 'https://stat4market.com',
#     'Connection': 'keep-alive',
#     'Referer': 'https://stat4market.com/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'cross-site',
# }
#
#
# def fetch_data(keyword):
#     encoded_keyword = quote(keyword)
#
#     url = f'https://calc.stat4market.app/analysis/sales/searchSelection/getSearchSelectionByName?search={encoded_keyword}'
#
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#
#         if data.get('success'):
#             name = data['data'].get('Name', '')
#             print(name)
#             frequency_rate = data['data'].get('FrequencyRate', 0)
#             items_count = data['data'].get('ItemsCount', 0)
#             dynamics_pct = data['data'].get('DynamicsPct', 0)
#             result = [name, '', frequency_rate, items_count, dynamics_pct]
#     except Exception as e:
#         print(f"Error fetching data for keyword '{keyword}': {e}")
#     return result
#
#
# # Используем ThreadPoolExecutor для параллельных запросов
# result = []
#
#
# def main():
#     # Создаем DataFrame и записываем заголовки
#     df = pd.DataFrame(columns=['Name', 'Category', 'FrequencyRate', 'ItemsCount', 'DynamicsPct'])
#     df.to_csv('output.csv', mode='w', index=False, sep=";", encoding='utf-8-sig')
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
#         futures = {executor.submit(fetch_data, keyword): keyword for keyword in keywords}
#
#         for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
#             keyword = futures[future]
#             try:
#                 result = future.result()
#                 print(f"Processed {count}/{len(keywords)}: {keyword}")
#
#                 # Добавляем результат в DataFrame и сохраняем в CSV
#                 with lock:
#                     df = pd.DataFrame([result], columns=['Name', 'Category', 'FrequencyRate', 'ItemsCount', 'DynamicsPct'])
#                     df.to_csv('output.csv', mode='a', header=False, index=False, sep=";", encoding='utf-8-sig')
#             except Exception as exc:
#                 print(f"Ошибка при обработке {keyword}: {exc}")

# with ThreadPoolExecutor(max_workers=12) as executor:
#     futures = {executor.submit(fetch_data, keyword): keyword for keyword in keywords}
#
#     for future in as_completed(futures):
#         result = future.result()
#
#     # Создаем DataFrame и сохраняем в Google Sheets
#     df = pd.DataFrame(result, columns=['Name', 'Category', 'FrequencyRate', 'ItemsCount', 'DynamicsPct'])
#
#     # Пример сохранения в файл, заменить на сохранение в Google Sheets
#     df.to_csv('output.csv', mode="a", index=False, sep=";", encoding='utf-8-sig')
#     print("Data has been saved to output.csv")


import requests
import json
import pandas as pd
import concurrent.futures
from urllib.parse import quote
from threading import Lock

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Origin': 'https://stat4market.com',
    'Connection': 'keep-alive',
    'Referer': 'https://stat4market.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

# Читаем ключевые слова из файла
with open('keys_new.txt', 'r', encoding='utf-8') as f:
    keywords = [line.strip() for line in f]

lock = Lock()


def fetch_data(keyword):
    encoded_keyword = quote(keyword)
    url = f'https://calc.stat4market.app/analysis/sales/searchSelection/getSearchSelectionByName?search={encoded_keyword}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get('success'):
            name = data['data'].get('Name', '')
            frequency_rate = data['data'].get('FrequencyRate', 0)
            items_count = data['data'].get('ItemsCount', 0)
            dynamics_pct = data['data'].get('DynamicsPct', 0)
            result = [name, '', frequency_rate, items_count, dynamics_pct]
        else:
            result = [keyword, '', 0, 0, 0]
    except Exception as e:
        print(f"Error fetching data for keyword '{keyword}': {e}")
        result = [keyword, '', 0, 0, 0]

    return result


def main():
    # Создаем DataFrame и записываем заголовки
    # df = pd.DataFrame(columns=['Name', 'Category', 'FrequencyRate', 'ItemsCount', 'DynamicsPct'])
    # df.to_csv('output_final.csv', mode='w', index=False, sep=";", encoding='utf-8-sig')

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(fetch_data, keyword): keyword for keyword in keywords}

        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            keyword = futures[future]
            try:
                result = future.result()
                print(f"Processed {count}/{len(keywords)}: {keyword}")

                # Добавляем результат в DataFrame и сохраняем в CSV
                with lock:
                    df = pd.DataFrame([result], columns=['Name', 'Category', 'FrequencyRate', 'ItemsCount', 'DynamicsPct'])
                    df.to_csv('output_final.csv', mode='a', header=False, index=False, sep=";", encoding='utf-8-sig')
            except Exception as exc:
                print(f"Ошибка при обработке {keyword}: {exc}")


if __name__ == "__main__":
    main()

