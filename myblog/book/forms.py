#django.forms.ModelFormを継承する場合
from django.forms import widgets
from .models import Book, Category, Author, Publisher
from django import forms
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin, UpdateView
from django.http import Http404
from django.db.models import Prefetch
# from . import forms
# from betterforms.multiform import MultiModelForm
from django.db.models import Q
import datetime

MONTHS = {}
for i in range(1,12):
    MONTHS[i] = i


class BookForm(forms.ModelForm):

    pages_low = forms.IntegerField(label='[本] ページ数', required=False,
        widget=forms.TextInput(attrs={
            'id': 'pages_low',
            'placeholder':'0',
            'pattern':'^[0-9]+$'}))

    pages_high = forms.IntegerField(label="～", label_suffix = " ", required=False,
        widget=forms.TextInput(attrs={
            'id': 'pages_high',
            'placeholder':'500',
            'pattern':'^[0-9]+$',}))

    issue_low = forms.IntegerField(label='[本] 発行日', required=True, initial="1900-1-1",
        widget=forms.SelectDateWidget(empty_label=None, months=MONTHS, years=[x for x in range(1900, datetime.date.today().year+1)], attrs={
            'id': 'issue_low',
            'pattern':'^[0-9]+$',
            'class':'fs-6_5'
        }))

    issue_high = forms.IntegerField(label="～", label_suffix = " ", required=True, initial=datetime.date.today(),
        widget=forms.SelectDateWidget(empty_label=None , months=MONTHS, years=[x for x in range(1900, datetime.date.today().year+1)], attrs={
            'id': 'issue_high',
            'pattern':'^[0-9]+$',
            'class':'fs-6_5'
        }))

    def __init__(self, *args, **kwd):
        super(BookForm, self).__init__(*args, **kwd)
        self.fields["title"].required = False
        self.fields["title"].label = "[本] タイトル"
        self.fields["title"].initial = ""
        
        

        self.label_suffix = " "
        self.labels = None



    class Meta:
        model = Book
        fields = ('title',)
        widgets = {
            'title'   : forms.TextInput(attrs={'placeholder': '虹を待つ彼女'}),
        }
class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwd):
        super(CategoryForm, self).__init__(*args, **kwd)
        self.fields["category"].required = False
        self.fields["category"].label = "[本] カテゴリー"
        self.label_suffix = " "
        # self.fields['category'].empty_label = '未選択'
    
    class Meta:
        model = Category
        fields = ('category',)
        widgets = {
            "category": forms.CheckboxSelectMultiple(attrs={'class': 'd-inline-block form-inline mb-2'})
            }


class AuthorForm(forms.ModelForm):
    age_low = forms.IntegerField(label="[著者] 生年月日",  required=True, initial="1900-1-1",
        widget=forms.SelectDateWidget(empty_label=None, months=MONTHS, years=[x for x in range(1900, datetime.date.today().year+1)], attrs={
            'id': 'age_low',
            'class':'fs-6_5'
            }))
    
    age_high = forms.IntegerField(label="～", label_suffix = " ", required=True, initial=datetime.date.today(),
        widget=forms.SelectDateWidget(empty_label=None, months=MONTHS, years=[x for x in range(1900, datetime.date.today().year+1)], attrs={
            'id': 'age_high',
            'class':'fs-6_5'
            }))

    def __init__(self, *args, **kwd):
        super(AuthorForm, self).__init__(*args, **kwd)
        self.fields["author"].required = False
        self.fields["sex"].required = False
        self.fields['sex'].empty_label = '未選択'
        # self.fields["sex"].help_text = "0以上120以下"
        self.fields["sex"].label="[著者] 性別"
        self.fields["author"].label="[著者] 名前"
        self.label_suffix = " "
        self.fields['sex'].choices.insert(0, ('','-----a----' ) )
        
        
    class Meta:
        model = Author
        fields = ('author', 'sex')
        widgets = {
            "sex": forms.RadioSelect(attrs={'placeholder': '[著者] 性別', 'class': 'form-inline'}),
            'author'   : forms.TextInput(attrs={'placeholder': '逸木裕'}),
        }

class PublisherForm(forms.ModelForm):
    choices=[(i.publisher_eng, i.publisher) for i in Publisher.objects.all()]
    publisher = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-inline-block form-inline mb-2'}))

    def __init__(self, *args, **kwd):
        super(PublisherForm, self).__init__(*args, **kwd)
        self.fields["publisher"].required = False
        self.fields["publisher"].label = "[出版社] 出版社"
        self.label_suffix = " "
        # self.fields['category'].empty_label = '未選択'
    
    class Meta:
        model = Publisher
        fields = ('publisher',)
        
        # widgets = {
        #     "publisher": forms.CheckboxSelectMultiple(attrs={'class': 'd-inline-block form-inline mb-2'})
        #     }
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        #     'text': forms.Textarea(attrs={'class': 'editable'})
        #     # cssクラスの追加(titleにtextinputclass, textにeditableクラスが追加されるようになります)
        # }



        # self.initial = None
        # self.fields['issue'].queryset = Publisher.objects
        # self.fields["category_info"].required = forms.CheckboxSelectMultiple()
        # self.fields["publisher_info"].required = False
        # self.fields['pages'].required = False
        # self.fields['issue'].required = False

        # validators=[validators.RegexValidator(
        #     regex=u'^[ぁ-んァ-ヶー一-龠]+\u3000[ぁ-んァ-ヶー一-龠]+$',
        #     message='氏名は漢字・ひらがな・カタカナのみとし、氏と名の間に全角スペースを入れてください',
        # )



# self.fields['category_id'].empty_label = '未選択'

        # widgets = {
        #             "name": forms.TextInput(attrs={'placeholder':'紀伊　太郎'}),
        #             "age": forms.RadioSelect(),

        #           }


        # author_age = Author(instance='age')
        # self.fields['author_age'] = author_age

# class UserProfileMultiForm(forms.MultiModelForm):
#     form_classes = {
#         'user': UserForm,
#         'profile': ProfileForm,
#     }




# class CategoryForm(forms.ModelForm):

#     def __init__(self, *args, **kwd):
#         super(CategoryForm, self).__init__(*args, **kwd)
#         self.fields["contents"].required = False

#     class Meta:
#         model = Category
#         fields = ("contents",)
#         widgets = {
#             'contents': forms.Textarea(attrs={'rows':15, 'cols':60}),
        # }




# #django.forms.ModelFormを継承する場合
# from .models import Manage, Category, Member
# from django import forms

# class VideosearchFrom(forms.ModelForm):

#     def __init__(self, *args, **kwd):
#         super(VideosearchFrom, self).__init__(*args, **kwd)
#         self.fields["youtube_video_title"].required = False
#         self.fields["category_id"].required = False
#         # self.fields["youtube_video_episode"].required = False
#         # self.fields["youtube_video_day"].required = False
#         self.fields["members"].required = False
#         self.fields['category_id'].empty_label = '未選択'
#         self.fields['members'].widget = forms.CheckboxSelectMultiple()  # 引数にattrs={'class': 'form-control'}も勿論できる。
#         self.fields['members'].queryset = Member.objects
#         # self.fields['members'].widget.attrs["class"] = "checkbox-inline radio-inline w-100"

#     class Meta:
#         model = Manage
#         # fields = ('youtube_video_title','category_id','youtube_video_episode','youtube_video_day','members') 
#         fields = ('youtube_video_title','category_id','members') 

# class CategoryForm(forms.ModelForm):

#     def __init__(self, *args, **kwd):
#         super(CategoryForm, self).__init__(*args, **kwd)
#         self.fields["contents"].required = False

#     class Meta:
#         model = Category
#         fields = ("contents",)
#         widgets = {
#             'contents': forms.Textarea(attrs={'rows':15, 'cols':60}),
#         }




