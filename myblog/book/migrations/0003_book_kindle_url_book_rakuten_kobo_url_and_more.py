# Generated by Django 4.1.1 on 2022-10-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='kindle_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='kindleURL'),
        ),
        migrations.AddField(
            model_name='book',
            name='rakuten_kobo_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='楽天KOBOURL'),
        ),
        migrations.AddField(
            model_name='book',
            name='rakuten_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='楽天URL'),
        ),
    ]
