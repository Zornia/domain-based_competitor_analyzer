from typing import Any, Dict, Optional

def extract_report_data(raw_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Извлекает из сырых WHOIS-данных 9 ключевых полей для отчёта.
    
    Параметры:
        raw_data (dict | None): сырой ответ от whois (результат w.__dict__)
    
    Возвращает:
        dict: словарь с 9 полями:
            - domain_name
            - registrant
            - registrar
            - registration_date
            - expiration_date
            - last_updated_date
            - name_servers
            - status
            - country
    
    Если поле отсутствует в сырых данных, возвращается None.
    """
    if raw_data is None:
        # Если сырых данных нет, возвращаем все поля как None
        return {
            "domain_name": None,
            "registrant": None,
            "registrar": None,
            "registration_date": None,
            "expiration_date": None,
            "last_updated_date": None,
            "name_servers": None,
            "status": None,
            "country": None,
        }

    def get_value(*keys: str) -> Any:
        """
        Возвращает первое найденное значение по списку возможных ключей.
        Если ни один ключ не найден — возвращает None.
        Это защищает от падений, если имя поля отличается (например, registrar vs registrar_name).
        """
        for key in keys:
            if key in raw_data:
                val = raw_data[key]
                # Если значение — список из одного элемента, часто удобнее вернуть сам элемент
                if isinstance(val, list) and len(val) == 1:
                    return val[0]
                return val
        return None

    # Извлечение 9 полей с учётом возможных вариантов названий ключей
    domain_name = get_value("domain_name", "domain")
    registrant = get_value(
        "registrant_name",
        "registrant",
        "name",  # иногда владелец лежит просто в name
        "person",
    )
    registrar = get_value("registrar", "registrar_name", "sponsor", "sponsoring_registrar")
    registration_date = get_value("creation_date", "registered_date")
    expiration_date = get_value("expiration_date", "expires")
    last_updated_date = get_value("updated_date", "last_updated")
    name_servers = get_value("name_servers", "name_server", "nameservers", "nameserver")
    status = get_value("status", "domain_status")
    country = get_value("country", "country_code", "registrant_country")

    return {
        "domain_name": domain_name,
        "registrant": registrant,
        "registrar": registrar,
        "registration_date": registration_date,
        "expiration_date": expiration_date,
        "last_updated_date": last_updated_date,
        "name_servers": name_servers,
        "status": status,
        "country": country,
    }


if __name__ == "__main__":
    # Блок для быстрой проверки модуля (не для работы приложения!)
    print("=== Запуск тестов data_processor ===")

    # Тест 1: сырые данные отсутствуют
    result_none = extract_report_data(None)
    assert all(v is None for v in result_none.values()), "Тест 1 не пройден: при None все поля должны быть None"
    print("Тест 1 (None) — OK")

    # Тест 2: «пустые» сырые данные (пустой словарь)
    result_empty = extract_report_data({})
    assert all(v is None for v in result_empty.values()), "Тест 2 не пройден: пустой dict должен давать все None"
    print("Тест 2 (пустой dict) — OK")

    # Тест 3: сырые данные с одним полем
    raw_with_one = {"domain_name": "test.com"}
    result_one = extract_report_data(raw_with_one)
    assert result_one["domain_name"] == "test.com"
    assert result_one["registrant"] is None
    assert result_one["registrar"] is None
    print("Тест 3 (одно поле) — OK")

    # Тест 4: сырые данные с разными вариантами названий ключей
    raw_variants = {
        "domain": "variant.com",
        "registrant_name": "Ivan Ivanov",
        "registrar_name": "REG.RU",
        "creation_date": "2020-01-01",
        "expiration_date": "2025-01-01",
        "updated_date": "2023-05-10",
        "nameservers": ["ns1.example.com", "ns2.example.com"],
        "status": "active",
        "country_code": "RU",
    }
    result_variants = extract_report_data(raw_variants)
    assert result_variants["domain_name"] == "variant.com"
    assert result_variants["registrant"] == "Ivan Ivanov"
    assert result_variants["registrar"] == "REG.RU"
    assert result_variants["name_servers"] == ["ns1.example.com", "ns2.example.com"]
    assert result_variants["country"] == "RU"
    print("Тест 4 (разные названия ключей) — OK")

    print("=== Все тесты data_processor пройдены ===")