from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import ModelFormMixin, UpdateView
from django.http import Http404
from django.db.models import Prefetch
from django.db.models import Q
import datetime
# from . import forms


from .models import Book, Category, Author, Publisher, Series, Templates, Other


import os
import platform










def common(request):
    # pf = platform.system()    
    
    context = {}
    # context['primary'] = Category.objects.all().first()
    # context['date_now'] = datetime.datetime.now()
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
    # context['others'] = Other.objects.filter(fin=1)
    context['others'] = Other.objects.all()

    context['author'] = Author.objects.all()
    context['book'] = Book.objects.filter(fin=1).order_by('-post_day')

    dict_ = {x:x.post_day for x in context['book']} | {x:x.post_day for x in context['others']}
    list_ = sorted(dict_.items(), key=lambda x:x[1] ,reverse=True)
    list_to_dict_ = dict(list_)
    context['books_others'] = list_to_dict_.keys()

        
        

    # context['author'] = []
    # set_count = [Book.objects.filter(author_info=a).count for a in Author.objects.all()]
    # if pf == 'Windows':
    #     context['google_analytics'] = 0
    # else:
    #     context['google_analytics'] = 1
        
    # for a in range(1, len(Author.objects.all())):
        # context['author'].append(Author.objects.values()[a] | {'category_count':set_count[a-1]})




    context['publisher'] = Publisher.objects.all()
    # context['templates'] = Templates.objects.all()

    #---  パンくずリスト作成　---
    url_path = request.path
    url_split = url_path.split('/')
    url_path = ""
    url_dict = {}
    url_dict = {"ホーム": "{0}://{1}/".format(request.scheme, request.get_host())}
    url_list = [{
                "title_info": "ホーム",
                "url_path_":"{0}://{1}/".format(request.scheme, request.get_host()),
                "icon_":"mdi-home",
            }]

    flag = 0
    url_path = "{0}://{1}/".format(request.scheme, request.get_host())
    try:

        context["url_main"] = None
        context['title_author_flag']  = 0
        for item in url_split[1:]:
            if item == "" :
                continue
            url_path += item + "/"

            if flag != 0:
                if context['title_info']  == "書籍一覧":
                    item = Book.objects.get(post_day=item).title
                    context['title_info'] = item
                    icon = "mdi-book-open-page-variant"

                elif context['title_info']  == "その他 記事":
                    item = Other.objects.get(post_day=item).title
                    icon = "mdi-checkbox-blank-circle-outline"
                    context['title_info'] = item
                    
                # context["url_sub"] = item
                # elif item == "book-ic":
                #     context['title_info']  = "BOOK I.C.について"
                # elif item == "profile":
                #     context['title_info']  = "プロフィール"
                # elif item == "books":
                #     context['title_info']  = "書籍一覧"
                # elif item == "others":
                #     context['title_info']  = "その他 記事"
                # elif item == "privacypolicy":
                #     context['title_info']  = "プライバシーポリシー"
                # elif item == "contact":
                #     context['title_info']  = "問い合わせ"


                url_list.append({
                    "title_info": context['title_info'],
                    "url_path_":url_path,
                    "icon_":icon,
                    })
                context['breadcrumb'] = url_list # パンくずリスト完成
                return context

            if item == "book":
                context['title_info'] = "ホーム"
                icon = "mdi-home"
            elif item == "book-ic":
                context['title_info']  = "BOOK I.C.について"
                icon = "mdi-office-building-marker-outline"
            elif item == "profile":
                context['title_info']  = "プロフィール"
                icon = "mdi-account-circle-outline"
            elif item == "books":
                icon = "mdi-office-building-marker-outline"
                context['title_info']  = "書籍一覧"
                icon = "mdi-bookshelf"
            elif item == "others":
                context['title_info']  = "その他 記事"
                icon = "mdi-dots-horizontal-circle-outline"
            elif item == "privacypolicy":
                context['title_info']  = "プライバシーポリシー"
                icon = "mdi-shield-lock-outline"
            elif item == "contact":
                context['title_info']  = "問い合わせ"
                icon = "mdi-email-outline"
            elif item == "sitemap":
                context['title_info']  = "サイトマップ"
                icon = "mdi-sitemap-outline"
            flag = 1

            url_list.append({
                
                "title_info": context['title_info'],
                "url_path_":url_path,
                "icon_":icon
                
                })
            context["url_sub"] = context['title_info']


        context['breadcrumb'] = url_list # パンくずリスト完成
    except:
        context['breadcrumb'] = url_list
        pass
    
    return context








#  2022/10/23 
#   try:
#         context["url_main"] = None
#         context['title_author_flag']  = 0
#         for item in url_split[1:]:
#             if item == "" :
#                 continue
#             url_path += item + "/"

#             if flag != 0 :
#                 print("■■■■■comon■")
#                 if flag == 1:
#                     item = Book.objects.get(post_day=item).title
#                     context['title_info'] = item
#                 if flag == 2:
#                     item = Category.objects.get(category=item).get_category_display
#                     context['title_info'] = item
#                 if flag == 3:
#                     item = Author.objects.get(author_eng=item).author
#                     context['title_info'] = item
#                 if flag == 4:
#                     item = Publisher.objects.get(publisher_eng=item).publisher
#                     context['title_info'] = item
#                 # context["url_main"] = item
#                 if flag == 5:
#                     item = "今後の予定（ToDo LIST）"
#                     context['title_info'] = item
#                 url_dict.update({item:url_path})
#                 context['breadcrumb'] = url_dict # パンくずリスト完成
#                 return context

#             if item == "book":
#                 item = "ホーム"
#                 context['title_info'] = item
#             if item == "books":
#                 item = '書籍一覧'
#                 flag = 1
#                 context['nav_active'] = flag
#                 context['title_info'] = item
#             if item == "categorys":
#                 item = "カテゴリー一覧"
#                 flag = 2
#                 context['nav_active'] = flag
#                 context['title_info'] = item
#             if item == "authors":
#                 item = "著者一覧"
#                 flag = 3
#                 context['nav_active'] = flag
#                 context['title_info'] = item
#             if item == "publishers":
#                 item = "出版社一覧"
#                 flag = 4
#                 context['nav_active'] = flag
#                 context['title_info'] = item
#             if item == "others":
#                 item = "その他"
#                 flag = 5
#                 context['nav_active'] = flag
#                 context['title_info'] = item

#             if flag == 1:
#                 context['title_author_flag']  = 1


#             url_dict.update({item:url_path})
#             context["url_sub"] = item
#         context['breadcrumb'] = url_dict # パンくずリスト完成
#     except:
#         context['breadcrumb'] = url_dict
#         pass
    
#     return context
