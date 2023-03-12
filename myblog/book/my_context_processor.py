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



from django.conf import settings






def common(request):
    # pf = platform.system()

    # ----  基本リスト取得-----
    context = {}
    context['category_list'] = Category.objects.all().order_by('category')
    context['author_list_Aa'] = [Author.objects.filter(word_oder='Aa').order_by("author"),
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
    context['other_list'] = Other.objects.all().filter(fin=1).order_by('-post_day')

    context['author_list'] = Author.objects.all()
    context['book_list'] = Book.objects.filter(fin=1).order_by('-post_day')

    dict_ = {x:x.post_day for x in context['book_list']} | {x:x.post_day for x in context['other_list']}
    list_ = sorted(dict_.items(), key=lambda x:x[1] ,reverse=True)
    list_to_dict_ = dict(list_)
    context['book_other_list'] = list_to_dict_.keys()

    context['publisher_list'] = Publisher.objects.all()


    context['book_info'] = ""
    context['other_info'] = ""

    #-------------





    #---  パンくずリスト作成　---
    url_path = request.path
    url_split = url_path.split('/')
    url_path = ""
    url_dict = {}
    url_dict = {"ホーム": "{0}://{1}/".format(request.scheme, request.get_host())}
    context['title_info'] = "ホーム"
    url_list = [{
                "title_info": "ホーム",
                "url_path_":"{0}://{1}/".format(request.scheme, request.get_host()),
                "icon_":"mdi-home",
            }]

    flag = 0
    url_path = "{0}://{1}/".format(request.scheme, request.get_host())

    context["url_sub"] = ""

    try:

        context["url_main"] = None
        context['title_author_flag']  = 0
        for item in url_split[1:]:
            if item == "" :
                continue
            url_path += item + "/"
            if flag != 0:                
                if context['title_info']  == "書籍一覧":
                    context['book_info'] = Book.objects.get(post_day=item)
                    item = Book.objects.get(post_day=item).title
                    context['title_info'] = item
                    icon = "mdi-book-open-page-variant"

                    url_list.append({
                        "title_info": context['title_info'],
                        "url_path_":url_path,
                        "icon_":icon,
                        })

                    


                    break


                elif context['title_info']  == "その他 記事":
                    context['other_info'] = Other.objects.get(post_day=item)
                    item = Other.objects.get(post_day=item).title
                    # icon = "mdi-checkbox-blank-circle-outline"
                    icon = ""
                    context['title_info'] = item



                url_list.append({
                    "title_info": context['title_info'],
                    "url_path_":url_path,
                    "icon_":icon,
                    })
                context['breadcrumb'] = url_list # パンくずリスト完成
                break
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

    # ------------




    # ----  book_info_next and book_info_prev 作成 （book_info and other_info） ---- #
    if context['other_info'] != None and context['other_info'] != "":
        context['other_info_prev'] = ""
        context['other_info_next'] = ""
        flag = False
        for item in context['other_list']:
            if flag:
                context['other_info_prev'] = item
                break
            if item.title == context['other_info'].title:
                flag = True
                continue
            context['other_info_next'] = item    

    if context['book_info'] != None and context['book_info'] != "":
        context['book_info_prev'] = ""
        context['book_info_next'] = ""
        flag = False
        for item in context['book_list']:
            if flag:
                context['book_info_prev'] = item
                break
            if item.title == context['book_info'].title:
                flag = True
                continue
            context['book_info_next'] = item    


    # --------------------------------------------------------------------------------



    # ----- contents text ------
    context['contents_pages_max'] = 0

    if len(url_list)==3:
        try:
            if context["url_sub"] == "書籍一覧":
                item = context['book_info']
            elif context["url_sub"] == "その他 記事":
                item = context['other_info']

            contents_page = request.path.split("/")[-2]
            contents_list_index = [0]
            count_title = 1

                
            context['contents_text'] = item.contents
            list_ = []
            count = 0
            for text_,i in zip(context['contents_text'].split('<')[1:], range(len(context['contents_text'].split('<')[1:]))):
                count += 1
                text_ = text_.split(">")
                # text_[0]
                contents_split = text_[1].splitlines()
                if text_[0] == "blockquote":
                    contents_ = "<a>" + contents_split[0] + "<br>" + "</a>"
                    for text_el in contents_split[1:]:
                        if text_el == "":
                            continue
                        contents_ = contents_ + "<a>"+ text_el +"<br>" + "</a>"
                        # print("contents_split", contents_split)
                else:
                    contents_ = contents_split[0]
                    for text_el in contents_split[1:]:
                        if text_el == "":
                            continue
                        contents_ = contents_ + text_el
                        # print("contents_split", contents_split)

                text_[1] = contents_
                
                if len(text_) == 3 and text_[0] == "blockquote":
                    text_[2] = text_[2].splitlines()[0]

                if text_[0] == "title":
                    count_title += 1
                    contents_list_index.append(count)
                    text_.append(str(count_title))
                    text_.append(str(count-contents_list_index[int(count_title-1)]+1))
                    # print("!!!count", count)
                    # print("!!!count_title", count_title)
                    # print("!!!contents_list_index[int(count_title-1)])", contents_list_index[int(count_title-1)]+1)

                if text_[0] == "subtitle":
                    text_.append(str(count_title))
                    try:
                        if count_title != 1:
                            text_.append(str(count-contents_list_index[int(count_title-1)]+1))
                        else: 
                            text_.append(str(count-contents_list_index[int(count_title-1)]))
                    except:
                        text_.append(str(count))
                        

                    # print("!!!!!!count", count)
                    # print("!!!!!!count_title", count_title)
                    # print("!!!!!!contents_list_index[int(count_title-1)])", contents_list_index[int(count_title-1)]+1)

                # print(text_)

                list_.append(text_)
            # print(list_)
            context['book_info_contents'] = list_
            
            if int(len(contents_list_index)) == int(contents_page):
                context['book_info_contents_page'] = list_[contents_list_index[int(contents_page)-1]-1:]
            elif int(contents_page) == 1:
                context['book_info_contents_page'] = list_[contents_list_index[int(contents_page)-1]:contents_list_index[int(contents_page)]-1]
            else:
                context['book_info_contents_page'] = list_[contents_list_index[int(contents_page)-1]-1:contents_list_index[int(contents_page)]-1]
            # print(context['book_info_contents_page'])
            count_subtitle = 0
            contents_subtitle_index = []
            for item in context['book_info_contents_page']:
                if item[0] == "subtitle":
                    count_subtitle += 1
                    if count_subtitle%2 == 1: 
                        contents_subtitle_index.append(item[3])
                context['contents_subtitle_index'] = contents_subtitle_index


            context["contents_page"] = contents_page
            context['contents_pages_max'] = str(count_title)
            context['contents_list_index'] = contents_list_index[2]
            context['count_index'] = "0"
            # print("contents_list_indexcontents_list_index", list_[contents_list_index[contents_page]:contents_list_index[contents_page+1]-1])
            # print("contents_list_indexcontents_list_index", list_[1:2])
            # print("contents_page",contents_list_index[int(contents_page)])
            # print("contents_list_indexcontents_list_index", list_[contents_list_index[int(contents_page)-1]:contents_list_index[int(contents_page)+1]])
            count = 0
            count_subtitle = 0
            for text_ in list_:
                count += 1
                if text_[0] == "subtitle":
                    count_subtitle += 1
                    if count_subtitle == 3:
                        break
        except:pass
            # context['count_subtitle'] = count

#---------------------------------------

#---- contents page select ----

    # contents_page = request.path.split("/")[-2]
    # for item in context['book_info_contents']:

        




    '''

    context['contents_text'] = context['book_info'].contents
    list_ = []
    count = 0
    for text_ in context['contents_text'].split('<')[1:]:
        count += 1
        text_ = text_.split(">")
        # text_[0]
        contents_split = text_[1].splitlines()
        if text_[0] == "blockquote":
            contents_ = "<a>" + contents_split[0] + "<br>" + "</a>"
            for text_el in contents_split[1:]:
                if text_el == "":
                    continue
                contents_ = contents_ + "<a>"+ text_el +"<br>" + "</a>"
                # print("contents_split", contents_split)
        else:
            contents_ = contents_split[0]
            for text_el in contents_split[1:]:
                if text_el == "":
                    continue
                contents_ = contents_ + text_el
                # print("contents_split", contents_split)

        text_[1] = contents_
        if len(text_) == 3:
            text_[2] = text_[2].splitlines()[0]
        list_.append(text_)
    context['book_info_contents'] = list_
    count = 0
    count_subtitle = 0
    for text_ in list_:
        count += 1
        if text_[0] == "subtitle":
            count_subtitle += 1
            if count_subtitle == 3:
                break
    context['count_subtitle'] = count
    except:
        pass



    '''


    # --------------------------------------------------------------------------------




    # print("context['book_info_contents'] ===", context['book_info_contents'])


    # ----- book_info_content page取得 ------
    # book_info_content = []
    # book_info_content_page = url_split[3]
    # count = 0
    # try:
    #     if url_split[3] != "":
    #         book_info_content_page = url_split[3]

    #         for item in context['book_info_contents']:
    #             if item[0] == "title":
    #                 print("flagtitle", count)
    #                 count += 1
    #             if int(book_info_content_page) == count:
    #                 book_info_content.append(item)
    #     context['book_info_contents'] = book_info_content
            

    # except:pass
        
        
    






    context['DEBUG'] = settings.DEBUG
    
    
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
