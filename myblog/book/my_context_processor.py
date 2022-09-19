from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import ModelFormMixin, UpdateView
from django.http import Http404
from django.db.models import Prefetch
from django.db.models import Q
import datetime
# from . import forms


from .models import Book, Category, Author, Publisher, Series, Templates


import os
import platform









def common(request):
    pf = platform.system()    
    
    context = {}
    # context['primary'] = Category.objects.all().first()
    context['date_now'] = datetime.datetime.now()
    context['category'] = Category.objects.all().order_by('category')
    context['author_Aa'] = [Author.objects.filter(word_oder='Aa').order_by("author"),
                                Author.objects.filter(word_oder='Ka').order_by("author"),
                                Author.objects.filter(word_oder='Sa').order_by("author"),
                                Author.objects.filter(word_oder='Ta').order_by("author"),
                                Author.objects.filter(word_oder='Na').order_by("author"),
                                Author.objects.filter(word_oder='Ha').order_by("author"),
                                Author.objects.filter(word_oder='Ma').order_by("author"),
                                Author.objects.filter(word_oder='Ya').order_by("author"),
                                Author.objects.filter(word_oder='Ra').order_by("author"),
                                Author.objects.filter(word_oder='Wa').order_by("author")
                                ]
    context['author'] = Author.objects.all()
    context['book'] = Book.objects.order_by('-post_day')
    # context['author'] = []
    set_count = [Book.objects.filter(author_info=a).count for a in Author.objects.all()]
    if pf == 'Windows':
        context['google_analytics'] = 0
    else:
        context['google_analytics'] = 1
        
    # for a in range(1, len(Author.objects.all())):
        # context['author'].append(Author.objects.values()[a] | {'category_count':set_count[a-1]})




    context['publisher'] = Publisher.objects.all()
    context['templates'] = Templates.objects.all()

    #---  パンくずリスト作成　---
    url_path = request.path
    url_split = url_path.split('/')
    url_path = ""
    url_dict = {}
    flag = 0
    url_path = "{0}://{1}/".format(request.scheme, request.get_host())
    try:
        context["url_main"] = None
        context['title_author_flag']  = 0
        for item in url_split[1:]:
            if item == "":
                continue
            url_path += item + "/"

            if flag != 0 :
                print("■■■■■comon■")
                if flag == 1:
                    item = Book.objects.get(post_day=item).title
                    context['title_info'] = item
                if flag == 2:
                    item = Category.objects.get(category=item).get_category_display
                    context['title_info'] = item
                if flag == 3:
                    item = Author.objects.get(author_eng=item).author
                    context['title_info'] = item
                if flag == 4:
                    item = Publisher.objects.get(publisher_eng=item).publisher
                    context['title_info'] = item
                # context["url_main"] = item
                if flag == 5:
                    item = "今後の予定（ToDo LIST）"
                    context['title_info'] = item
                url_dict.update({item:url_path})
                context['breadcrumb'] = url_dict # パンくずリスト完成
                return context

            if item == "book":
                item = "ホーム"
                context['title_info'] = item
            if item == "books":
                item = '書籍一覧'
                flag = 1
                context['nav_active'] = flag
                context['title_info'] = item
            if item == "categorys":
                item = "カテゴリー一覧"
                flag = 2
                context['nav_active'] = flag
                context['title_info'] = item
            if item == "authors":
                item = "著者一覧"
                flag = 3
                context['nav_active'] = flag
                context['title_info'] = item
            if item == "publishers":
                item = "出版社一覧"
                flag = 4
                context['nav_active'] = flag
                context['title_info'] = item
            if item == "others":
                item = "その他"
                flag = 5
                context['nav_active'] = flag
                context['title_info'] = item

            if flag == 1:
                context['title_author_flag']  = 1


            url_dict.update({item:url_path})
            context["url_sub"] = item

        context['breadcrumb'] = url_dict # パンくずリスト完成
    except:
        pass
    

        
    return context
