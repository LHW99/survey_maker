# Generated by Django 3.1.2 on 2020-11-21 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]