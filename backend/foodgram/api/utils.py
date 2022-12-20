from datetime import date


def make_shopping_list(input_objects, user):
    result = []
    result.append(
        f'Foodgram - список покупок\n'
        f'Пользователь: {user.first_name} {user.last_name}\n'
        f'Дата: {date.today().strftime("%d.%m.%Y")}\n\n'
    )
    for item in input_objects:
        result.append(
            f'{item["ingredient__name"]} '
            f'({item["ingredient__measurement_unit"]}) - '
            f'{item["amount"]}\n'
        )
    return ''.join(result)
