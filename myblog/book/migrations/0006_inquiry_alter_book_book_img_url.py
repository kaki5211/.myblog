# Generated by Django 4.1.1 on 2022-10-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_book_book_img_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('mail_add', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('inquiry', models.TextField(verbose_name='問い合わせ内容')),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='book_img_url',
            field=models.TextField(blank=True, null=True, verbose_name='商品画像'),
        ),
    ]
