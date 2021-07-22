from django import template

register = template.Library()


@register.filter(name='none_attribute')
def none_filter_attribute(value):
    if value is None:
        return 'Non définit'
    else:
        listValue: list = value.split('-')
        return ' '.join(word.capitalize() for word in listValue)
