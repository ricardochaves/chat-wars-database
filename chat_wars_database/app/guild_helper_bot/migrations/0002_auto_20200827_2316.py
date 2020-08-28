# Generated by Django 3.1 on 2020-08-27 23:16

import chat_wars_database.app.guild_helper_bot.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild_helper_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('delete_command', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.FloatField(unique=True),
        ),
        migrations.CreateModel(
            name='InvitationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_id', models.UUIDField(db_index=True, default=chat_wars_database.app.guild_helper_bot.models.hex_uuid)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_helper_bot.guild')),
            ],
        ),
        migrations.AddField(
            model_name='guild',
            name='captain',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='guild_helper_bot.telegramuser'),
        ),
        migrations.CreateModel(
            name='UserGuild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Member'), (2, 'Admin')], default=1)),
                ('leave_command', models.CharField(blank=True, max_length=100, null=True)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_helper_bot.guild')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_helper_bot.telegramuser')),
            ],
            options={
                'unique_together': {('user', 'guild')},
            },
        ),
    ]