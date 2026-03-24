from django import forms
from django_summernote.widgets import SummernoteWidget

from todo.models import Comment, ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "img",
        )
        widgets = {
            "description": SummernoteWidget(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "img",
            "is_completed",
        )
        widgets = {
            "description": SummernoteWidget(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-checkbox-input"}),
            "img": forms.FileInput(attrs={"class": "form-control"}),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("message",)
        widgets = {
            "message": forms.TextInput(attrs={"class": "rows cols form-control"})
        }
        labels = {"message": "내용"}
