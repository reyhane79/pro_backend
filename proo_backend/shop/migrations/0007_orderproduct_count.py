# Generated by Django 3.2.5 on 2022-12-12 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_reply_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
