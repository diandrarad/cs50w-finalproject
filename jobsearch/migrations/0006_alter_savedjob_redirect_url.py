# Generated by Django 4.2.1 on 2023-05-26 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsearch', '0005_alter_savedjob_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedjob',
            name='redirect_url',
            field=models.URLField(),
        ),
    ]