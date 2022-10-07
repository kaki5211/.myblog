from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
# from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static



from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import resolve_url
from django.urls import path, include
from .models import Book
import datetime


app_name='book'

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Book.objects.all()

    def location(self, obj):
        data_info=(obj.post_day).strftime("%Y-%m-%d")
        # data_info= obj.post_day
        return resolve_url('book:book_info', data_info=data_info)

    def lastmod(self, obj):
        return obj.post_day

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('', views.TopView.as_view(), name="top"),
    path('quasar/', views.TopquasarView.as_view(), name="top_quasar"),

    path('categorys/', views.CategoryView.as_view(), name='category'),# 本のカテゴリー
    path('categorys/<slug:data_info>', views.CategoryView.as_view(), name='category_infprofile', ),

    path('authors/', views.AuthorView.as_view(), name='author'), # 著者について全般
    path('authors/<data_info>', views.AuthorView.as_view(), name='author_info'),

    path('publishers/', views.PublisherView.as_view(), name='publisher'), # 出版社情報
    path('publishers/<slug:data_info>', views.PublisherView.as_view(), name='publisher_info'),

    path('series/', views.SeriesView.as_view(), name='series'), # シリーズもの本
    path('series/<slug:data_info>', views.SeriesView.as_view(), name='series_info'), 

    path('books/', views.BookView.as_view(), name='book'), # 主に本の検索と
    path('books/<slug:data_info>', views.BookView.as_view(), name='book_info'), 

    path('search', views.SearchView.as_view(), name='search' ), # 本の検索全般

    path('articles/', views.ArticlesView.as_view(), name='article'), # トピックスに近いもの

    path('otherss/', views.OthersView.as_view(),  name='other'),
    path('others/shedule', views.Schedule.as_view(),  name='schedule'),

    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('book-ic/', views.Book_icView.as_view(), name="book-ic"),
    path('others', views.OthersView.as_view(), name="others"),
    path('privacypolicy', views.Privacy_policyView.as_view(), name="privacy_policy"),
    path('contact', views.ContactView.as_view(), name="contact"),
    

    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},  name='sitemap'),

    path('test/', views.test_,  name='test_'),
    
    # path('base', views.TestView.as_view(), name="base"),


    ]





""" 予定-----------------------------
top
    -Recently （最近の投稿）
    -auther（著者）一覧のみ[（あいうえお順）/（男・女）/（年齢）]
        -著者の情報　＋　Book[カテゴリー/出版日]
    -Publisher（出版社）一覧のみ
        -出版社の情報　＋　Author[（あいうえお順）/（男・女）/（年齢）]
    -category（カテゴリー）
    -読む予定の本一覧
    -外部リンク[アリクイちゃんねる/技術コンテンツ/ヨウヘイ]

search
    -カテゴリー
    -出版社
    -著者
    -日付

-----------------------------"""

