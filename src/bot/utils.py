from pytils import translit


def transliteration(string) -> str:
    """Transliterate the name into Latin with prefix 'profession_'."""
    profession = translit.translify(string).lower()
    prefix = "profession_"
    result = prefix + profession
    return result
