# Generated by Django 4.1.4 on 2022-12-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birdnestapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilotdata',
            name='createdDt',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pilotdata',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='pilotdata',
            name='firstName',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pilotdata',
            name='lastName',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pilotdata',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='pilotdata',
            name='pilotId',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
