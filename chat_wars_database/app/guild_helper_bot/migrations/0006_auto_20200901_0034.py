# Generated by Django 3.1 on 2020-09-01 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guild_helper_bot', '0005_guildchannel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiddenheadquarter',
            name='combination',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='hiddenlocation',
            name='combination',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
