# Generated by Django 3.2.7 on 2021-09-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BooleanSearch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.TextField(default='Sample text.', max_length=200000, null=True),
        ),
    ]
