from django import forms

from todo.models import Comment, ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
        )


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "is_completed",
        )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("message",)
        widgets = {
            "message": forms.TextInput(attrs={"class": "rows cols form-control"})
        }
        labels = {"message": "내용"}
