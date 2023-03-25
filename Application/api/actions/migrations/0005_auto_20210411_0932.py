# Generated by Django 3.0.7 on 2021-04-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210316_2035'),
        ('actions', '0004_remove_action_uuid_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='assigned_volunteers',
            field=models.ManyToManyField(blank=True, help_text='Volunteers who have been assigned to completing the action..', related_name='actions_assigned_to', to='users.Volunteer'),
        ),
        migrations.AddField(
            model_name='action',
            name='maximum_volunteers',
            field=models.SmallIntegerField(default=1, help_text='maximum number of volunteers required for action'),
        ),
        migrations.AddField(
            model_name='action',
            name='minimum_volunteers',
            field=models.SmallIntegerField(default=1, help_text='minimum number of volunteers required for action'),
        ),
    ]