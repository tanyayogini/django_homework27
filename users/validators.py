from datetime import date

from django.core.exceptions import ValidationError

MIN_AGE = 9
FORBIDDEN_DOMAINS = ["rambler.ru"]

def check_birth(value):
    today = date.today()
    age = (today.year - value.year - 1) + ((today.month, today.day) >= (value.month, value.day))
    if age < MIN_AGE:
        raise ValidationError(f"You cannot register if you are under {MIN_AGE}")


def check_domains(value):
    for domain in FORBIDDEN_DOMAINS:
        if domain in value:
            raise ValidationError(f"You cannot register with {domain} domain")
