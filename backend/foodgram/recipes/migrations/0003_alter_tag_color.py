# Generated by Django 3.2.16 on 2022-12-19 12:51

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221216_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', help_text='Укажите HEX-код цвета тега', image_field=None, max_length=7, samples=None, verbose_name='Цвет в HEX'),
        ),
    ]
