# Generated by Django 4.1.3 on 2022-11-27 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_discipline_options_student_gender_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['fio']},
        ),
    ]
