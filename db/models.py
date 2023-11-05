from mongoengine import (
    StringField,
    Document,
    DateTimeField,
    FloatField
)

from datetime import datetime


class Currency(Document):
    """Model for Currency."""

    meta = {"collection": "Currency", "indexes": [{"fields": ["-from_currency"]}]}
    from_currency = StringField(max_length=3)
    to_currency = StringField(max_length=3)
    amount = FloatField()
    convert_value = FloatField()
    createdDate = DateTimeField(default=datetime.utcnow)


class Measure(Document):
    temperature = FloatField()
    humidity = FloatField()
    createdDate = DateTimeField(default=datetime.utcnow)