import re

from django import template

register = template.Library()


@register.filter
def format_telefone(value):
    """Formata (11) 98765-4321 para celular e (11) 3333-4444 para fixo."""
    if not value:
        return ''
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return value


@register.filter
def remove_chars(value):
    """Deixa apenas os digitos, para montar o link do WhatsApp."""
    if not value:
        return ''
    return re.sub(r'\D', '', str(value))
