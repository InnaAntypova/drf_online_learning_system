from rest_framework import serializers


class URLValidator:
    """ Валидация на соответствие вводимого url """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        print(tmp_val)
        if tmp_val is None:
            return None

        if 'youtube.com' not in tmp_val.lower():
            raise serializers.ValidationError('Недопустимый URL адрес!')
