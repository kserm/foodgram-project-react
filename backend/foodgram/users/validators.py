from django.core.exceptions import ValidationError


def validate_name_me(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Имя "me" недопустимо.',
            params={"value": value},
        )
