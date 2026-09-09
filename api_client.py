import whois

def fetch_whois_data(domain: str) -> dict:
    """
    Запрашивает данные WHOIS для указанного домена.
    
    Параметры:
        domain (str): доменное имя (например, google.com)
    
    Возвращает:
        dict: {
            "success": bool,
            "data": dict | None,
            "error": str | None
        }
    """
    try:
        w = whois.whois(domain)
        # dict(w) даёт все распарсенные поля (registrar, creation_date и т.д.),
        # а w.__dict__ — только domain и text (остальные свойства через @property)
        raw_data = dict(w)
        return {
            "success": True,
            "data": raw_data,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


if __name__ == "__main__":
    print("=== Запуск тестов api_client ===")

    # Тест 1: валидный домен с полными данными
    res_ok = fetch_whois_data("google.com")
    assert res_ok["success"] is True, "Тест 1 не пройден: ожидался success=True для google.com"
    assert res_ok["data"] is not None, "Тест 1 не пройден: data должен быть не None"

    data = res_ok["data"]
    has_domain = "domain_name" in data or "domain" in data
    has_dates = any(k in data for k in ("creation_date", "expiration_date", "updated_date"))
    assert has_domain, "Тест 1 не пройден: нет поля domain_name/domain"
    assert has_dates, "Тест 1 не пройден: нет дат (creation/expiration/updated)"
    print("Тест 1 (валидный домен) — OK")

    # Тест 2: несуществующий домен
    res_fail = fetch_whois_data("this-domain-definitely-does-not-exist-999.com")
    assert res_fail["success"] is False, "Тест 2 не пройден"
    assert res_fail["data"] is None, "Тест 2 не пройден: data должен быть None"
    assert isinstance(res_fail["error"], str), "Тест 2 не пройден: error должен быть строкой"
    print("Тест 2 (несуществующий домен) — OK")

    # Тест 3: пустая строка
    res_empty = fetch_whois_data("")
    assert res_empty["success"] is False, "Тест 3 не пройден"
    assert res_empty["data"] is None
    print("Тест 3 (пустая строка) — OK")

    # Тест 4: None
    res_none = fetch_whois_data(None)
    assert res_none["success"] is False, "Тест 4 не пройден"
    assert res_none["data"] is None
    print("Тест 4 (None) — OK")

    print("=== Все тесты пройдены ===")