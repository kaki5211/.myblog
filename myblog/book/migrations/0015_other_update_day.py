# Generated by Django 4.1.1 on 2022-10-23 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_other_contents_synopsis'),
    ]

    operations = [
        migrations.AddField(
            model_name='other',
            name='update_day',
            field=models.DateField(blank=True, null=True, verbose_name='更新日'),
        ),
    ]
