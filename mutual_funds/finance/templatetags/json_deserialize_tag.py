import json

from django import template


register = template.Library()


def decerialise_json(json_string):
    return json.loads(json_string)


register.filter('decerialise_json', decerialise_json)
