# Generated by Django 2.0 on 2020-02-25 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workprogramsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workprogram',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, null=True, related_name='WorkProgramPrerequisites', through='workprogramsapp.PrerequisitesOfWorkProgram', to='dataprocessing.Items'),
        ),
    ]