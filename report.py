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
        # Если список из одного элемента — показывает просто элемент
        if len(value) == 1:
            return str(value[0])
        # Иначе — через запятую (для серверов имён и т.д.)
        return ", ".join(str(v) for v in value)

    return str(value)


def print_report(data: Dict[str, Any]) -> None:

    """Выводит отчёт по домену в читаемом виде"""

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
        # data.get(key) — безопасный доступ: если ключа нет, вернётся None, а не ошибка.
        raw_value = data.get(key)
        # format_value превращает сырые данные в понятную строку.
        formatted_value = format_value(raw_value)
        # f"{label:<35}" — выравнивание названия по левому краю в поле шириной 35 символов.
        # Благодаря этому все двоеточия встают ровно в одну вертикальную линию.
        print(f"{label:<35} : {formatted_value}")

    print("=" * 60 + "\n")