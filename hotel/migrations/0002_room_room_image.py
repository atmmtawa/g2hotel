# Generated by Django 5.0.6 on 2024-06-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_image',
            field=models.FileField(null=True, upload_to='rooms/'),
        ),
    ]
