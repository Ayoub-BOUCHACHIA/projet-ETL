# Generated by Django 4.1.5 on 2023-01-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_product', models.IntegerField()),
                ('id_category', models.IntegerField()),
                ('id_provider', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
