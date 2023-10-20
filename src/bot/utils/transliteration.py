from pytils import translit


def transliteration(string: str, prefix: str = "") -> str:
    """Transliterate the string into Latin with prefix."""
    translit_string = translit.translify(string).lower()
    result = prefix + translit_string
    return result
