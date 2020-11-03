from django import template

register = template.Library()


@register.filter(name='bytesToString')
def bytesToString(memory):
    return str(memory.tobytes())[2:-1]
