from django.contrib import admin

from .models import NewsPost, NewsCategory


class NewsPostInline(admin.TabularInline):
    model = NewsCategory.posts.through
    extra = 0
    classes = ('grp-collapse',)

    def has_add_permission(self, request):
        return False


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['title']
    inlines = [NewsPostInline]


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'pub_date', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('category',)
    list_filter = ['is_active', 'category']
    list_display_links = ['title']
