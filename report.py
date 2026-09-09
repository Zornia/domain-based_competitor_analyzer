from typing import Any, Dict

def format_value(value: Any) -> str:
    """
    Превращает любое значение в читаемую строку.
    - Если значение None → возвращает «Не указано»
    - Если это список → превращает в строку через запятую
    - Иначе → просто приводит к строке
    """
    if value is None:
        return "Не указано"

    if isinstance(value, list):
        # Если список из одного элемента — показываем просто элемент
        if len(value) == 1:
            return str(value[0])
        # Иначе — через запятую (для серверов имён и т.д.)
        return ", ".join(str(v) for v in value)

    return str(value)


def print_report(data: Dict[str, Any]) -> None:
    """
    Выводит отчёт по домену в читаемом виде.

    Параметры:
        data (dict): словарь с 9 полями от data_processor.extract_report_data
    """
    # Отображаемые названия полей (человекопонятные)
    labels = {
        "domain_name": "Доменное имя",
        "registrant": "Владелец / организация",
        "registrar": "Регистратор",
        "registration_date": "Дата регистрации",
        "expiration_date": "Дата истечения",
        "last_updated_date": "Дата последнего обновления",
        "name_servers": "Серверы имён (DNS)",
        "status": "Статус домена",
        "country": "Страна регистранта",
    }

    print("\n" + "=" * 60)
    print("ОТЧЁТ ПО ДОМЕНУ")
    print("=" * 60)

    for key, label in labels.items():
        raw_value = data.get(key)
        formatted_value = format_value(raw_value)
        print(f"{label:<35} : {formatted_value}")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Блок для быстрой проверки модуля (не для работы приложения!)
    print("=== Запуск тестов report.py ===\n")

    # Тест 1: все поля заполнены
    full_data = {
        "domain_name": "example-site.com",
        "registrant": "ООО «Пример»",
        "registrar": "REG.RU",
        "registration_date": "2020-05-10",
        "expiration_date": "2026-05-10",
        "last_updated_date": "2024-03-01",
        "name_servers": ["ns1.reg.ru", "ns2.reg.ru"],
        "status": "active",
        "country": "RU",
    }
    print("Тест 1 — полный отчёт:")
    print_report(full_data)

    # Тест 2: много полей отсутствует (симуляция приватности)
    partial_data = {
        "domain_name": "private-domain.com",
        "registrant": None,
        "registrar": None,
        "registration_date": None,
        "expiration_date": None,
        "last_updated_date": None,
        "name_servers": None,
        "status": None,
        "country": None,
    }
    print("Тест 2 — отчёт с отсутствующими данными:")
    print_report(partial_data)

    # Тест 3: список серверов имён из нескольких элементов
    multi_ns_data = {
        "domain_name": "multi-ns.com",
        "registrant": "Ivan Ivanov",
        "registrar": "Beget",
        "registration_date": "2019-01-01",
        "expiration_date": "2025-01-01",
        "last_updated_date": None,
        "name_servers": ["ns1.beget.com", "ns2.beget.com", "ns3.beget.com"],
        "status": "ok",
        "country": "RU",
    }
    print("Тест 3 — отчёт с несколькими серверами имён:")
    print_report(multi_ns_data)

    print("=== Тесты report.py пройдены ===")