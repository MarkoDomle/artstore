# Generated by Django 4.2.1 on 2023-08-31 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(upload_to='pictures'),
        ),
    ]
