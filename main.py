from api_client import fetch_whois_data
from data_processor import extract_report_data
from report import print_report

def main():
    print("Получение данных о сайте по домену")
    print("Введите доменное имя (например, google.com) или 'q' для выхода.\n")

    while True:
        domain = input("Домен: ").strip().lower()

        # Выход по q/quit
        if domain in ("q", "quit", "exit"):
            print("Выход из программы")
            break

        # Проверка на пустой ввод
        if not domain:
            print("Ошибка: доменное имя не может быть пустым. Попробуйте ещё раз.\n")
            continue

        # Получаем сырые данные через API-клиент
        response = fetch_whois_data(domain)

        if not response["success"]:
            print(f"Не удалось получить данные: {response['error']}")
            print("Возможные причины: нет интернета, домен не найден, сервер недоступен.\n")
            continue

        # Обрабатываем данные (вытаскиваем 9 полей)
        processed = extract_report_data(response["data"])

        # Выводим отчёт
        print_report(processed)