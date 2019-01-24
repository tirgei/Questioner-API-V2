import re
from marshmallow import ValidationError
from datetime import datetime


def required(value):
    """Validate that field under validation does not contain null value"""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('This field cannot be empty')
        return value


def password(password):
    """ Validate password is Strong """

    message = 'Password should contain atleast 1 small letter, 1 capital\
    letter, 1 character and 1 digit'

    if len(password) < 8:
        raise ValidationError(message)

    scores = {}

    for letter in password:
        if letter.islower():
            scores['has_lower'] = 1

        if letter.isupper():
            scores['has_upper'] = 1

        if letter.isdigit():
            scores['has_digit'] = 1

    if sum(scores.values()) < 3:
        raise ValidationError(message)

    elif ' ' in password:
        raise ValidationError('Password should not contain any spaces')


def date(date):
    """ Function to validate meetup date """

    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/([12][0-9]{3})$", date):
        raise ValidationError('Date should be in the format dd/mm/yyyy')

    date_format = "%d/%m/%Y"
    date = datetime.strptime(date, date_format)
    now = datetime.now()

    if date < now:
        raise ValidationError('Date should not be in the past')


def tags(tags):
    """ Validate meetup tags are present """

    if not tags and not len(tags) > 0:
        raise ValidationError('You need to pass atleast 1 tag for the meetup')

    else:
        for tag in tags:
            required(tag)


def phonenumber(phone):
    """ Validate phone number """

    if not re.match('^[0-9]*$', phone):
        raise ValidationError('Phone number should be digits only')

    elif len(phone) < 10:
        raise ValidationError('Phone number should be atleast 10 digits')


def name(name):
    """ Validate name """

    if not name.isalpha():
        raise ValidationError('Name should contain only letters')
