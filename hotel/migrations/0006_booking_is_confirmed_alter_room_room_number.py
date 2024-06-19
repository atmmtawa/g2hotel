# Generated by Django 5.0.6 on 2024-06-19 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_fooditem_remove_customuser_is_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]