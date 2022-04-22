from re import match

from django.core.validators import ValidationError


def hex_code_validator(value):
    pattern = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not match(pattern, value):
        raise ValidationError(
            'HEX-код должен состоять из 6 символов и начинаться с #'
        )
