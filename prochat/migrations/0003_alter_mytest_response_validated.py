# Generated by Django 5.0.6 on 2024-06-27 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prochat', '0002_alter_mytest_response_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytest',
            name='Response_validated',
            field=models.CharField(max_length=40000),
        ),
    ]
