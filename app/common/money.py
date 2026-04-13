from decimal import Decimal, ROUND_HALF_UP

_MINOR_FACTOR = Decimal("100")
_MONEY_PRECISION = Decimal("0.01")

def to_minor_units(amount: Decimal) -> int:
	"""
	Converts sum in rubles into sum in kopecks

	:param amount: sum in rubles
	:return: sum in kopecks
	"""
	normalized = amount.quantize(_MONEY_PRECISION, rounding=ROUND_HALF_UP)
	return int(normalized * _MINOR_FACTOR)


def from_minor_unites(amount: int) -> Decimal:
	"""
	Converts sum in kopecks into sum in rubles

	:param amount: sum in kopecks
	:return: sum in rubles
	"""
	return (Decimal(amount) / _MINOR_FACTOR).quantize(_MONEY_PRECISION, rounding=ROUND_HALF_UP)