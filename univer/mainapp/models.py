from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass


class Direction(models.Model):
    name = models.CharField("Название направления", max_length=30)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Куратор")

    def __str__(self):
        return self.name

class Discipline(models.Model):
    name = models.CharField("Название дисциплины", max_length=30)
    directions = models.ManyToManyField(Direction, verbose_name="Направление", related_name='disciplines')

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name

class Group(models.Model):
    MAX_STUDENTS_COUNT = 20

    name = models.CharField("Название группы", max_length=30)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Направление")

    def __str__(self):
        return self.name


class Student(models.Model):

    class Meta:
        ordering = ['fio',]

    class Genders(models.TextChoices):
        MALE = 'M', _('мужской')
        FEMALE = 'F', _('женский')

    fio = models.CharField("ФИО студента", max_length=30)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа", related_name='students', null=True)
    gender = models.CharField("Пол", max_length=2, choices=Genders.choices, default = '', null=False)

    def __str__(self):
        return self.fio
