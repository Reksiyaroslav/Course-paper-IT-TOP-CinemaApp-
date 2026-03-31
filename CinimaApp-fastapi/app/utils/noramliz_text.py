from typing import Dict, Any


def text_strip_lower(text: str) -> str:
    if text is None:
        return ""
    return text.strip().lower()


def text_strip(text: str):
    if text is None:
        return ""
    return text.strip()


def no_change(value: Any) -> Any:
    return value


NORMAL_CONFING = {
    "actor": {
        "fistname": text_strip_lower,
        "lastname": text_strip_lower,
        "patronymic": text_strip_lower,
        "birth_date": no_change,
        "star": no_change,
    },
    "author": {
        "fistname": text_strip_lower,
        "lastname": text_strip_lower,
        "patronymic": text_strip_lower,
        "birth_date": no_change,
        "bio": text_strip,
    },
    "film": {"title": text_strip, "description": text_strip, "release_date": no_change},
    "user": {
        "username": text_strip_lower,
        "email": text_strip_lower,
        "password": no_change,
    },
    "type_film": {"type_film_name": text_strip_lower},
    "country": {
        "country_name": text_strip_lower,
    },
    "comment": {
        "description": text_strip,
    },
}


def normalize_data(data: Dict[str, Any], model_type: str) -> Dict[str, Any]:
    cofing = NORMAL_CONFING.get(model_type, {})
    if not cofing:
        return data
    normalize = {}
    for filed, normalize_func in cofing.items():
        value = data.get(filed)
        normalize[filed] = normalize_func(value)
    for filed, value in data.items():
        if filed not in normalize:
            normalize[filed] = value
    return normalize
