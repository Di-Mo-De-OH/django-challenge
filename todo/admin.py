from django.contrib import admin

from .models import Comment, ToDo

# Register your models here.


admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["message", "user"]
    extra = 1


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    inlines = [CommentInline]
