# Generated by Django 4.1.7 on 2023-07-14 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('category', '0003_alter_category_description'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='product',
            new_name='Products',
        ),
    ]
