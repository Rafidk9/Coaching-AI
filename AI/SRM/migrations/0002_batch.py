# Generated by Django 4.2.5 on 2023-09-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('schedule', models.CharField(max_length=100)),
            ],
        ),
    ]