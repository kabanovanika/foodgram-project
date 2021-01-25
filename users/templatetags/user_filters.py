from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag
def query_transform(request, **kwargs):
    print('я сюда зашел')
    updated = request.GET.copy()
    print(updated)
    for k, v in kwargs.items():
        print(k, v)
        if v is not None:
            updated[k] = v
            print(f'новый урл {updated.urlencode()}')
        else:
            updated.pop(k, 0)  # Remove or return 0 - aka, delete safely this key
    return updated.urlencode()
