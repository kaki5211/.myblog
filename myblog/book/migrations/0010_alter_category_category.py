# Generated by Django 4.1.1 on 2022-10-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_alter_inquiry_inquiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, choices=[('action', 'アクション'), ('adventure', 'アドベンチャー'), ('youth', '青春'), ('love', '恋愛'), ('sf', 'SF'), ('history', '時代'), ('mystery', 'ミステリー'), ('comedy', 'コメディー'), ('horror', 'ホラー')], default=None, max_length=20, null=True, verbose_name='カテゴリー'),
        ),
    ]
