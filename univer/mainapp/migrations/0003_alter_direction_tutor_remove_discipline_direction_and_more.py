# Generated by Django 4.1.3 on 2022-11-24 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_direction_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Куратор'),
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='direction',
        ),
        migrations.AddField(
            model_name='discipline',
            name='direction',
            field=models.ManyToManyField(related_name='disciplines', to='mainapp.direction', verbose_name='Направление'),
        ),
    ]
