# Generated by Django 3.2.5 on 2022-09-18 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20220918_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemcategory',
            old_name='Product',
            new_name='product',
        ),
    ]
