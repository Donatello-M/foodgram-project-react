from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),)
    personal_info = models.TextField(max_length=255, blank=True,
                                     verbose_name='Информация о себе')
    email = models.EmailField(null=False, unique=True, verbose_name='Эл.почта')

    class Meta:
        ordering = ('username',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        ordering = ('-user',)
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='uniques')]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
