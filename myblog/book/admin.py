from django.contrib import admin

# Register your models here.

from .models import Book, Author, Category,Series, Templates, Publisher


# admin.site.register(Manage)
# admin.site.register(Category)
# admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publisher)

# admin.site.register(BOOK)

# class BookAdmin(admin.ModelAdmin):
    # list_display = ('title' , 'pages', 'issue', 'author_info', 'category_info', 'publisher_info', 'fin')
    # fieldsets = [
    #     (None, {'fields': ['youtube_video_title']}),
    #     ('メンバー', {'fields': ['members'],}),
    #     ('#', {'fields': ['youtube_video_episode'],}),
    # ]

    # search_fields = ['youtube_video_title']
    # search_fields = ['youtube_video_category']
    # list_filter = ['members']
    # def get_categorys(self, obj):
    #     return "\n".join([p.category for p in obj.category_info.all()])









admin.site.register(Book)
admin.site.register(Series)
admin.site.register(Templates)

# admin.site.register(Publisher_label)






# サンプル--------------------------------------------------------------------
"""
admin.site.register(Contents_demo)




# class MwmberInline(admin.TabularInline):
#     model = Member
#     extra = 3

class ManageAdmin(admin.ModelAdmin):
    list_display = ('id' , 'youtube_video_title', 'youtube_video_episode', 'youtube_video_day', 'category_id')
    # fieldsets = [
    #     (None, {'fields': ['youtube_video_title']}),
    #     ('メンバー', {'fields': ['members'],}),
    #     ('#', {'fields': ['youtube_video_episode'],}),
    # ]

    search_fields = ['youtube_video_title']
    # search_fields = ['youtube_video_category']
    # list_filter = ['members']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "category_jp", "get_members")
    # fields = ['members']
    # fieldsets = [
    #     ("カテゴリーjp", {'fields':['category_jp']}),
    #     ("カテゴリーeng", {'fields':['category_eng']}),
    # ]
    def get_members(self, obj):
        return "\n".join([p.member_jp for p in obj.members.all()])

admin.site.register(Manage, ManageAdmin)

admin.site.register(Category, CategoryAdmin)


# class ManageAdmin(admin.ModelAdmin):

"""
# サンプル--------------------------------------------------------------------

