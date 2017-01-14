from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Profile, LikedFund
)


class LikedFundInline(admin.TabularInline):
    model = LikedFund
    extra = 1


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ('user', 'image_thumb', 'avatar_thumbnail', 'sex', 'birthday', 'slug', 'country', 'created_date', 'modified_date',)
    readonly_fields = ['image_thumb', 'created_date', 'modified_date']
    inline_classes = ('grp-open',)


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    inlines = [ProfileInline] + UserAdmin.inlines


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug',)
    search_fields = ('user__username',)
    fields = ('user', 'image_thumb', 'avatar_thumbnail', 'sex', 'birthday', 'slug', 'country', 'created_date', 'modified_date',)
    readonly_fields = ['image_thumb', 'created_date', 'modified_date']
    inlines = (LikedFundInline,)


@admin.register(LikedFund)
class LikedFundAdmin(admin.ModelAdmin):
    list_display = ('user', 'fund',)
    list_filter = ('user', 'fund',)
    search_fields = ('user__username', 'fund')
    fields = ('user', 'fund', 'created_date', 'modified_date',)
    readonly_fields = ['created_date', 'modified_date']
