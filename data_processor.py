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
        # Если сырых данных нет, возвращает все поля как None
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
        """

        for key in keys:
            if key in raw_data:
                val = raw_data[key]
                # Если значение — список из одного элемента, часто удобнее вернуть сам элемент
                if isinstance(val, list) and len(val) == 1:
                    return val[0]
                return val
        return None

    # Извлекает 9 полей с учётом возможных вариантов названий ключей
    domain_name = get_value("domain_name", "domain")
    registrant = get_value(
        "registrant_name",
        "registrant",
        "name",
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