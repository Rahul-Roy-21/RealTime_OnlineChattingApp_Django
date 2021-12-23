# Generated by Django 3.2.8 on 2021-11-02 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_messages_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='live_user',
            options={'ordering': ['user_id'], 'verbose_name': 'Live_User', 'verbose_name_plural': 'Live_Users'},
        ),
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 2, 18, 50, 31, 802694)),
        ),
    ]