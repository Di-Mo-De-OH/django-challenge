from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Comment, ToDo

# Register your models here.


admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["message", "user"]
    extra = 1


@admin.register(ToDo)
class ToDoAdmin(SummernoteModelAdmin):
    list_display = ("id", "title", "description")
    inlines = [CommentInline]
