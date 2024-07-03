import requests
import json
import concurrent.futures
from urllib.parse import quote
from threading import Lock
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Аутентификационный JSON-ключ, который вы загрузили в проект Google Apps Script
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'pythontablewb-e5ed696e1885.json',
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])

# Авторизация и открытие нужной таблицы
gc = gspread.authorize(credentials)
sheet = gc.open_by_key('165jW53ahz1zjph6tXg-2I9Rg1zcH44f0YXas9GHEkj0').sheet1  # Замените YOUR_SPREADSHEET_ID на ID вашей таблицы

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        future_to_keyword = {executor.submit(fetch_data, keyword): keyword for keyword in keywords}

        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                result = future.result()
                print(f"Processed: {keyword}")

                # Добавляем результат в Google Sheets
                with lock:
                    sheet.append_row(result)
            except Exception as exc:
                print(f"Ошибка при обработке {keyword}: {exc}")


if __name__ == "__main__":
    main()

