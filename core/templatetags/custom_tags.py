from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='dateFormat')
def dateFormat(value):
    d = datetime.strptime(value[:20], "%b %d %Y %H:%M:%S")
    return d.strftime("%Y.%m.%d")