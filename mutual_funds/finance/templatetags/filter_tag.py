from django import template


register = template.Library()


@register.simple_tag
def print_return(number=None):
    if number:
        if number == 30:
            return 'return 1 month'
        elif number == 90:
            return 'return 3 months'
        elif number == 180:
            return 'return half year'
        elif number == 1800:
            return 'return 5 years'
    else:
        return 'return 1 year'
