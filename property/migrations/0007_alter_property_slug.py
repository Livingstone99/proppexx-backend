# Generated by Django 3.2 on 2021-06-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_auto_20210620_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='slug',
            field=models.SlugField(editable=False, max_length=300, null=True),
        ),
    ]