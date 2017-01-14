from django import template


register = template.Library()


def prettify_percents(percents):
    return round((float(percents) - 1) * 100, 2)


register.filter('prettify_percents', prettify_percents)
