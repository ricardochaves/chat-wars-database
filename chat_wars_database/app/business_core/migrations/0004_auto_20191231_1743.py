# Generated by Django 3.0.1 on 2019-12-31 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_core', '0003_auto_20191230_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='modification_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='can_be_found_in_quests',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='craftable',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='depositable_in_guild',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='event_item',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='mana_crafting',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_foray_day',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_foray_evening',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_foray_morning',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_foray_night',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_forest_day',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_forest_evening',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_forest_morning',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_forest_night',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_swamp_day',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_swamp_evening',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_swamp_morning',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_swamp_night',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_valley_day',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_valley_evening',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_valley_morning',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quest_valley_night',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='skill_craft_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='tradeable_auction',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='tradeable_exchange',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
