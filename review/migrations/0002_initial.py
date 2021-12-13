# Generated by Django 3.2 on 2021-06-08 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
        ('team', '0001_initial'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='assiged_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.adminagent'),
        ),
        migrations.AddField(
            model_name='review',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property'),
        ),
    ]
