from datetime import datetime
from datetime import date

to_datetime = lambda s: datetime.fromisoformat(s)
to_date = lambda s: date.fromisoformat(s)

order_schema = {
    'id': {'type': 'integer', 'min': 0, 'coerce': int},
    'created_at': {'type': 'datetime', 'coerce': to_datetime},
    'vendor_id': {'type': 'integer', 'min': 0, 'coerce': int},
    'customer_id': {'type': 'integer', 'min': 0, 'coerce': int},
}

order_line_schema = {
    'order_id': {'type': 'integer', 'min': 0, 'coerce': int},
    'product_id': {'type': 'integer', 'min': 0, 'coerce': int},
    'product_description': {'type': 'string', 'coerce': str},
    'product_price': {'type': 'integer', 'min': 0, 'coerce': int},
    'product_vat_rate': {'type': 'float', 'min': 0.0, 'max': 1.0, 'coerce': float},
    'discount_rate': {'type': 'float', 'min': 0.0, 'max': 1.0, 'coerce': float},
    'quantity': {'type': 'integer', 'min': 0, 'coerce': int},
    'full_price_amount': {'type': 'integer', 'min': 0, 'coerce': int},
    'discounted_amount': {'type': 'number', 'min': 0, 'coerce': float},
    'vat_amount': {'type': 'number', 'min': 0, 'coerce': float},
    'total_amount': {'type': 'number', 'min': 0, 'coerce': float},
}

product_schema = {
    'id': {'type': 'integer', 'min': 0, 'coerce': int},
    'description': {'type': 'string', 'coerce': str},
}

promotion_schema = {
    'id': {'type': 'integer', 'min': 0, 'coerce': int},
    'description': {'type': 'string', 'coerce': str},
}

product_promotion_schema = {
    'date': {'type': 'date', 'coerce': to_date},
    'product_id': {'type': 'integer', 'min': 0, 'coerce': int},
    'promotion_id': {'type': 'integer', 'min': 0, 'coerce': int},
}

vendor_commissions_schema = {
    'date': {'type': 'date', 'coerce': to_date},
    'vendor_id': {'type': 'integer', 'min': 0, 'coerce': int},
    'rate': {'type': 'float', 'min': 0.0, 'max': 1.0, 'coerce': float},
}
