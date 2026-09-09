import whois

def fetch_whois_data(domain: str) -> dict:

    """Запрашивает данные WHOIS для указанного домена"""
    
    try:
        w = whois.whois(domain)
        # Важно: нужно использовать dict(w), а не w.__dict__ для преобразования в словарь.
        # Объект whois использует @property для полей (creation_date, registrar и др.),
        # поэтому w.__dict__ их не видит. dict(w) корректно возвращает все поля.
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