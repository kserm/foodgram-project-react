# Generated by Django 2.2.28 on 2022-12-16 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientlist',
            options={'verbose_name': 'Список ингрединтов', 'verbose_name_plural': 'Списки ингрединтов'},
        ),
    ]