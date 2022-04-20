from re import compile

from django.core.validators import ValidationError
from django.db import models


def hex_code_validator(value):
    pattern = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not compile(pattern, value):
        raise ValidationError(
            'HEX-код должен состоять из 6 символов и начинаться с #'
        )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        #validators=[hex_code_validator],
        verbose_name='Цвет, HEX-code',
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name
