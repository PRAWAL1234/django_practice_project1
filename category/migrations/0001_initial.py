# Generated by Django 4.1.7 on 2023-07-07 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, unique=True)),
                ('image', models.ImageField(upload_to='photo/categories')),
            ],
        ),
    ]
