from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.urls import reverse_lazy

from todo.models import ToDo

class ToDoListView(LoginRequiredMixin,ListView):
    model = ToDo
    queryset = ToDo.objects.all()
    template_name="todos/todo_list.html"
    paginate_by = 10
    ordering="-created_at"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)|
                Q(description__icontains=q)
            )
        
        return queryset
    

class ToDoDetailView(LoginRequiredMixin,DetailView):
    model = ToDo
    template_name ="todos/todo_info.html"

    def get_object(self, queryset = None):
        object = super().get_object()
        if object.user != self.request.user and not self.request.user.is_authenticated:
            raise Http404("당신이 작성한게 아닙니다.")
        return object
    
    def get_context_data(self,**kwargs):
        context = {"todo":self.object.__dict__}
        return context


class ToDoCreateView(LoginRequiredMixin,CreateView):
    model = ToDo
    template_name= "todos/todo_create.html"
    fields = ("title","description","start_date","end_date")

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy("todo:info",kwargs = {"pk":self.object.pk})
    

class ToDoUpdateView(LoginRequiredMixin,UpdateView):
    model = ToDo
    template_name = "todos/todo_update.html"
    fields = ("title","description","start_date","end_date","is_completed")

    def get_object(self, queryset = None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        if self.object.user != self.request.user:
            raise Http404()
        return self.object
    def get_success_url(self):
        return reverse_lazy("todo:info",kwargs={"pk":self.object.pk})
    

class ToDoDeleteView(LoginRequiredMixin,DeleteView):
    model = ToDo
    
    def get_object(self,queryset = None):
        object = super().get_object(queryset)
        if object.user != self.request.user and not self.request.user.is_authenticated:
            raise Http404("당신이 작성한 게시물이 아니라 삭제할 수 없습니다.")
            
        return object
        
    def get_success_url(self):
        return reverse_lazy("todo:list")