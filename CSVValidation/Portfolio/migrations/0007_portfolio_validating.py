# Generated by Django 2.2.3 on 2019-07-17 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0006_auto_20190717_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='validating',
            field=models.BooleanField(default=False),
        ),
    ]