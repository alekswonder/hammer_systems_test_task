# Generated by Django 4.2.4 on 2023-08-17 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='invite_code',
            field=models.CharField(default='Dx9`5W', max_length=6, unique=True),
        ),
    ]
