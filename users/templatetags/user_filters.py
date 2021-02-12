from django import template

from recipe.models import ShoppingList

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)
    return updated.urlencode()


@register.filter
def lookup(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def amount_of_purchases(user):
    counter = ShoppingList.objects.values_list('purchase_recipe_id',
                                               flat=True).filter(user_id=user)
    amount = counter.count()
    if amount == 0:
        amount = ''
    return amount


@register.simple_tag
def active_button(path_name, url_name):
    if path_name in url_name:
        return 'nav__item_active'
