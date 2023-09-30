from pytils import translit


def translation(string):
    """Translate the name into Latin with prefix 'profession_'."""
    profession = translit.translify(string).lower()
    prefix = "profession_"
    result = prefix + profession
    return result
