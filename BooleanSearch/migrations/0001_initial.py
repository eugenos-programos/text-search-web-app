# Generated by Django 3.2.7 on 2021-09-16 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=1000, null=True)),
                ('text', models.CharField(default='Sample text.', max_length=20000, null=True)),
                ('snippet', models.CharField(default='Sample snippet.', max_length=300, null=True)),
                ('url', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(default='Query', max_length=1000, null=True)),
            ],
        ),
    ]