# Generated by Django 4.1.1 on 2022-12-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_book_emb_instagram_book_emb_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='other',
            name='fin',
            field=models.BooleanField(blank=True, null=True, verbose_name='完読'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, choices=[('action', 'アクション'), ('adventure', 'アドベンチャー'), ('youth', '青春'), ('love', '恋愛'), ('sf', 'SF'), ('history', '時代'), ('mystery', 'ミステリー'), ('comedy', 'コメディー'), ('horror', 'ホラー'), ('bungaku', '文学')], default=None, max_length=20, null=True, verbose_name='カテゴリー'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_eng',
            field=models.CharField(blank=True, choices=[('action_eng', 'action'), ('adventure_eng', 'adventure'), ('youth_eng', 'youth'), ('love_eng', 'love'), ('sf_eng', 'sf'), ('history_eng', 'history'), ('mystery_eng', 'mystery'), ('comedy_eng', 'comedy'), ('horror_eng', 'horror'), ('bungaku_eng', 'bungaku')], max_length=20, null=True, verbose_name='カテゴリーeng'),
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('red', 'red'), ('orange', 'orange'), ('blue', 'blue'), ('pink', 'pink'), ('info', 'info'), ('green', 'green'), ('purple', 'purple'), ('warning', 'warning'), ('dark', 'dark'), ('blue-grey', 'blue-grey')], max_length=20, verbose_name='色'),
        ),
    ]
