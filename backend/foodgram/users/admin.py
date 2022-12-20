from django.contrib import admin
from users.models import Follow, User

EMPTY_VAL = '-empty-'


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'username',
        'email'
    )
    ordering = ('username',)
    empty_value_display = EMPTY_VAL


@admin.register(Follow)
class CustomFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author', 'user')
    list_filter = ('author', 'user')
    empty_value_display = EMPTY_VAL
