# Generated by Django 4.0.4 on 2022-06-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_alter_menu_countries_alter_page_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_external',
            field=models.BooleanField(default=False),
        ),
    ]
