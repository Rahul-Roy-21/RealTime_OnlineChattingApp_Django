# Generated by Django 3.2.8 on 2021-11-02 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_messages_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 2, 18, 38, 32, 592204)),
        ),
    ]
