# Generated by Django 4.1.1 on 2022-10-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='other',
            name='image',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
    ]
