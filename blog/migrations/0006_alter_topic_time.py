# Generated by Django 4.1.7 on 2023-03-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_topic_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
