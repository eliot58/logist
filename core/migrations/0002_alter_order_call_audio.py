# Generated by Django 5.0.1 on 2024-01-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='call_audio',
            field=models.FileField(blank=True, null=True, upload_to='audio', verbose_name='Результат созвона в аудио'),
        ),
    ]
