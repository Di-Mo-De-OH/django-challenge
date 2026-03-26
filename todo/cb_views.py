from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from todo.forms import CommentCreateForm, ToDoForm, TodoUpdateForm
from todo.models import Comment, ToDo


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDo
    queryset = ToDo.objects.all()
    template_name = "todos/todo_list.html"
    paginate_by = 10
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        return queryset


class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = "todos/todo_info.html"
    queryset = ToDo.objects.all().prefetch_related("comments", "comments__user")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("당신이 볼 수 없는 게시물 입니다")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.order_by("-created_at")
        paginator = Paginator(comments, 5)
        context["todo"] = self.object
        context["comment_form"] = CommentCreateForm()
        context["page_obj"] = paginator.get_page(self.request.GET.get("page"))
        return context


class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    template_name = "todos/todo_form.html"
    form_class = ToDoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.pk})


class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = "todos/todo_form.html"
    form_class = TodoUpdateForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        if self.object.user != self.request.user:
            raise Http404()
        return self.object

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.pk})


class ToDoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("당신이 작성한 게시물이 아니라 삭제할 수 없습니다.")

        return obj

    def get_success_url(self):
        return reverse_lazy("todo:list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    pk_url_kwarg = "todo_id"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = self.get_todo()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_todo(self):
        pk = self.kwargs["todo_id"]
        todo = get_object_or_404(ToDo, pk=pk)
        return todo

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.kwargs["todo_id"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ("message",)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404("수정할 수 없는 게시물 입니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.todo.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404("당신이 작성한 댓글이 아닙니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:list")
