from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.aggregates import Count
from django.db.models.enums import Choices
from django.db.models.fields import SmallIntegerField, TimeField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.validators import MinLengthValidator, RegexValidator
import datetime


# いらないｰｰｰｰｰｰｰｰ
# sex_ = (
#     ("man", '男性'),
#     ("woman", '女性')
# )
# ｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰ

# Create your models here.


class Book(models.Model):
    isbn13 = models.CharField(max_length=14,
                                validators=[MinLengthValidator(14, '文字数が一致していません。例）978-4167174033'),
                                            RegexValidator(r'[0-9]{3}[-][0-9]{10}', '形式に当てはまっていません。例）978-4167174033')], null=True, blank=True)

    title = models.CharField('タイトル', max_length=100, null=True, blank=True)
    pages = models.SmallIntegerField('ページ数', null=True, blank=True)
    issue = models.DateField('発行日', null=True, blank=True) # [発行日, y m d]

    post_day = models.DateField('投稿日', null=True, blank=True) # [投稿日, y m d]
    update_day = models.DateField('更新日', null=True, blank=True) # [投稿日, y m d]


    YOUTH_CHOICES = (('Y', 'Youth'),('O', 'Old'))
    youth_choices = models.CharField('青春/白秋', choices=YOUTH_CHOICES, max_length=10)

    series_info = models.ForeignKey("Series", verbose_name=("シリーズ情報"), on_delete=models.CASCADE, null=True, blank=True)
    author_info = models.ForeignKey("Author", verbose_name=("著者情報"), on_delete=models.CASCADE, null=True, blank=True)
    # category_info = models.ManyToManyField("Category", verbose_name=("カテゴリー情報"), blank=True, related_name="category_info")
    category_info = models.ForeignKey("Category", verbose_name=("カテゴリー情報"), blank=True,null=True,on_delete=models.CASCADE)

    publisher_info = models.ForeignKey("Publisher", verbose_name=("出版社情報"), on_delete=models.CASCADE, null=True, blank=True)
    publisher_label_info = models.ForeignKey("Publisher_label", verbose_name=("レーベル"), on_delete=models.CASCADE, null=True, blank=True)

    contents = models.TextField("コンテンツ", null=True, blank=True)
    contents_synopsis =  models.TextField("あらすじ", null=True, blank=True)

    fin = models.BooleanField('完読', null=True, blank=True)

    amazon_url = models.CharField('アマゾンURL', max_length=1000, null=True, blank=True)
    amazon_url_text = models.CharField('アマゾンURL_text', max_length=1000, null=True, blank=True)
    kindle_url = models.CharField('kindleURL', max_length=1000, null=True, blank=True)
    rakuten_url = models.CharField('楽天URL', max_length=1000, null=True, blank=True)
    rakuten_kobo_url = models.CharField('楽天KOBOURL', max_length=1000, null=True, blank=True)

    book_img_url = models.TextField('商品画像', null=True, blank=True)

    emb_twitter = models.CharField('twitter埋め込み',max_length=10000, null=True, blank=True)
    emb_instagram = models.CharField('instagram埋め込み',max_length=10000, null=True, blank=True)

    def to_dict(i, idex_list, self):
        dict_r = {}
        for index in idex_list:
            dict_ = {}
            # query_ = 'obj_.values_list("{}")[0]'.format(index)
            query_ = 'Book.objects.filter(fin=1).values_list("{}")[{}][0]'.format(index, i)
            if index == "category_info":
                query_ = 'Category.objects.get(id=Book.objects.filter(fin=1).values_list("{}")[{}][0]).get_category_display()'.format(index, i)
            elif index == "author_info":
                query_ = 'Author.objects.get(id=Book.objects.filter(fin=1).values_list("{}")[{}][0]).author'.format(index, i)
            elif index == "post_day":
                query_ = 'Book.objects.filter(fin=1).values_list("{}")[{}][0].strftime("%Y-%m-%d")'.format(index, i)
            exec("{} = {}".format(index, query_), globals(), dict_)
            dict_r = dict_r | dict_
        return dict_r

    def __str__(self):
        return self.title



class Author(models.Model):
    GENDER_CHOICES = (('Mon', '男性'),('Womon', '女性'))
    WORD_CHOICES = (('Aa', 'あ行'),('Ka', 'か行'),('Sa', 'さ行'),('Ta', 'た行'),('Na', 'な行'),('Ha', 'は行'),('Ma', 'ま行'),('Ya', 'や行'),('Ra', 'ら行'),('Wa', 'わ行'))

    author = models.CharField('著者', max_length=100, default=None) # 追加していく-----------
    author_eng = models.CharField('著者eng', max_length=100) # 追加していく-----------
    word_oder = models.CharField('五十音', choices=WORD_CHOICES, max_length=10)
    age = models.DateField('生年月日')
    sex = models.CharField('性別', choices=(('', '未選択'),)+GENDER_CHOICES, max_length=10, blank=True)
    contents = models.TextField("コンテンツ")
    contents_lite = models.TextField("コンテンツ", blank=True, null=True)

    post_day = models.DateField('投稿日', null=True) # [発行日, y m d]
    def __str__(self):
        return self.author
    
class Category(models.Model):
    CATEGORY_CHOICES = (('action', 'アクション'),('adventure', 'アドベンチャー'),('youth', '青春'),('love', '恋愛'),('sf', 'SF'),('history', '時代'),('mystery', 'ミステリー'),('comedy', 'コメディー'), ('horror', 'ホラー'), ('bungaku', '文学'))
    CATEGORYENG_CHOICES = (('action_eng', 'action'), ('adventure_eng', 'adventure'), ('youth_eng', 'youth'), ('love_eng', 'love'), ('sf_eng', 'sf'), ('history_eng', 'history'), ('mystery_eng', 'mystery'), ('comedy_eng', 'comedy'), ('horror_eng', 'horror'), (('bungaku_eng', 'bungaku')))
    # CATEGORYENG_CHOICES = (('action', 'アクション'),('adventure', 'アドベンチャー'),('youth', '青春'),('love', '恋愛'),('sf', 'SF'),('history', '時代'),('mystery', 'ミステリー'),('comedy', 'コメディー'), ('horror', 'ホラー'))
    COLOR_CHOICES = (('red', 'red'), ('orange','orange'),('blue', 'blue'), ('pink', 'pink'),('info','info'), ('green', 'green'), ('purple', 'purple'), ('warning','warning'),('dark', 'dark'), ('blue-grey', 'blue-grey'))

    category = models.CharField("カテゴリー", choices=CATEGORY_CHOICES, max_length=20, default=None, null=True, blank=True) # 追加していく-----------
    category_eng = models.CharField("カテゴリーeng", choices=CATEGORYENG_CHOICES ,max_length=20, null=True, blank=True) # 追加していく-----------
    color = models.CharField("色", choices=COLOR_CHOICES, max_length=20)
    color_hex = models.CharField("色_hex値", max_length=20,  blank=True)

    contents = models.TextField("コンテンツ", blank=True)
    contents_keyword = models.TextField("キーワード", blank=True)

    post_day = models.DateField('投稿日', null=True) # [発行日, y m d]
    def __str__(self):
        return self.category

class Publisher(models.Model):
    publisher = models.CharField('出版社', max_length=50)
    publisher_eng = models.CharField('出版社_eng', max_length=50, blank=True, null=True)
    contents = models.TextField("コンテンツ")
    incorporated = models.DateField('設立日')

    post_day = models.DateField('投稿日', null=True) # [発行日, y m d]
    def __str__(self):
        return self.publisher

class Publisher_label(models.Model):
    publisher = models.ForeignKey("Publisher", verbose_name=("出版者"), on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField("ラベル", max_length=20, default=None) # 追加していく-----------
    label_eng = models.CharField("ラベルeng", max_length=20, default=None) # 追加していく-----------
    def __str__(self):
        return self.label

class Series(models.Model):
    series = models.CharField("シリーズ", max_length=100)
    contents = models.TextField("コンテンツ")

    author = models.ForeignKey("Author", verbose_name=("著者"), on_delete=models.CASCADE)

    post_day = models.DateField('投稿日', null=True) # [発行日, y m d]
    def __str__(self):
        return self.series


class Inquiry(models.Model):
    id = models.AutoField("id", primary_key = True)
    name = models.CharField("ニックネーム", max_length=50)
    mail_add = models.EmailField("メールアドレス", max_length=254)
    inquiry = models.TextField("問い合わせ内容", max_length=2047)

class Other(models.Model):
    title = models.CharField('タイトル', max_length=100, null=True, blank=True)
    post_day = models.DateField('投稿日', null=True, blank=True) # [投稿日, y m d]
    update_day = models.DateField('更新日', null=True, blank=True) # [投稿日, y m d]
    
    image = models.ImageField(upload_to='media')
    contents = models.TextField("コンテンツ", null=True, blank=True)
    contents_synopsis =  models.TextField("あらすじ", null=True, blank=True)

    fin = models.BooleanField('完読', null=True, blank=True)

    def __str__(self):
        return self.title





class Templates(models.Model):
    breadcrumb = models.TextField("目次")

    










class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=500)

class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=500)
    Department = models.CharField(max_length=500)
    DateOfJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=500)







""" 予定 ----------------------------
作品タイトル
出版日
・y
・m
・d
ページ数
画像
感想（コンテンツ）


アマゾンリンク

■集英社
■カテゴリー
　※複数あり
■著者
・男/女
・生まれ年
・
----------------------------"""
