# Generated by Django 3.1 on 2020-08-29 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild_helper_bot', '0002_auto_20200827_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alliance_guild_owner', to='guild_helper_bot.guild')),
            ],
        ),
        migrations.AddField(
            model_name='guild',
            name='alliance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guild_helper_bot.alliance'),
        ),
    ]
