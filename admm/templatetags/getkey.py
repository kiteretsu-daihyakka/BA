from django import template

register=template.Library()
@register.filter(name='getkey')
def getkey(values,arg):
    return values[arg]