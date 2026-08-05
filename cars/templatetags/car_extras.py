from decimal import Decimal

from django import template

register = template.Library()


def _thousands(value):
    """12345 -> '12.345' (separador brasileiro)."""
    return f'{value:,}'.replace(',', '.')


@register.filter
def brl(value):
    """Preço no formato da vitrine: 89000.00 -> '89.000'.

    Centavos só aparecem quando existem de fato — num anúncio de carro
    'R$ 89.000,00' carrega dois zeros que ninguém lê.
    """
    if value is None:
        return 'Sob consulta'
    try:
        value = Decimal(value)
    except (TypeError, ArithmeticError, ValueError):
        return value

    inteiro, centavos = divmod(value.quantize(Decimal('0.01')), 1)
    texto = _thousands(int(inteiro))
    if centavos:
        texto += f',{int(centavos * 100):02d}'
    return texto


@register.filter
def km(value):
    """Quilometragem legível. 0 é informação (carro zero), None não é."""
    if value is None:
        return 'Km não informada'
    if value == 0:
        return '0 km'
    return f'{_thousands(int(value))} km'


@register.filter
def field_type(field):
    """Nome da classe do widget, para o template escolher o layout do campo."""
    return field.field.widget.__class__.__name__
