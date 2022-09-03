def get_ingredients_for_shopping(ingredients):
    shop_list = {}
    for ingredient in ingredients:
        amount = ingredient['amount__sum']
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        shop_list[name] = {
            'amount': amount,
            'measurement_unit': measurement_unit
        }
    out_list = ['Foodgram\n\n']
    for ingr, value in shop_list.items():
        out_list.append(
            f" {ingr} - {value['amount']} "
            f"{value['measurement_unit']}\n"
        )
    return out_list
