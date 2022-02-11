from datetime import date
from django.core.exceptions import ValidationError

def validate_birthday(value):
    if value >= date.today():
        raise ValidationError("Your birthday must be before today")
