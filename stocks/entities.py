# -*- coding: utf-8 -*-


class StockEntity:
    DEFAULT_FIELDS_RETURN = ['symbol', 'name', 'price']

    def __init__(self):
        self.symbol = None
        self.name = None
        self.price = None

    def as_dict(self, fields: list = None) -> dict:
        fields = fields or self.DEFAULT_FIELDS_RETURN
        stocks_dict = {}
        for field_name in fields:
            if hasattr(self, field_name):
                stocks_dict[field_name] = getattr(self, field_name)
        return stocks_dict
