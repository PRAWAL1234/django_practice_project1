# Generated by Django 4.1.7 on 2023-07-07 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='background')),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
