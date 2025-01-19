from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """A custom filter to retrieve values from a dictionary using a key."""
    return dictionary.get(key)
