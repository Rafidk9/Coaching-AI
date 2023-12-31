# Generated by Django 4.2.5 on 2023-09-22 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0002_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='last_recording_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='recordings_given',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='batch',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='batch',
            name='schedule',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='ClassRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('date', models.DateField()),
                ('topic', models.CharField(max_length=200)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SRM.batch')),
            ],
        ),
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_date', models.DateField()),
                ('class_recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SRM.classrecording')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SRM.student')),
            ],
        ),
    ]
