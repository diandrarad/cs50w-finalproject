# Generated by Django 4.2.1 on 2023-05-24 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobsearch', '0002_alter_application_id_alter_company_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listing',
            unique_together={('title', 'display_name')},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='country',
        ),
    ]
