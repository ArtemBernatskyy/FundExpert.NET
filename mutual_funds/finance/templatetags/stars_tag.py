from django import template


register = template.Library()


def draw_stars(number):
    empty_star = '<i class="ti-star"></i>'
    full_star = '<i class="fa fa-star"></i>'
    empty_count = 5 - int(number)
    return full_star * int(number) + empty_star * empty_count


register.filter('draw_stars', draw_stars)
