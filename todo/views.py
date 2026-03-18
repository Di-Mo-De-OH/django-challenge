from django.shortcuts import render,redirect
from django.urls import reverse
from todo.models import ToDo



# Create your views here.

def todo_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse("user_login"))
    todos = ToDo.objects.all()
    context = {
        "todos":todos
    }
    return render(request,"todos/todo_list.html",context)

def todo_info(request,todo_id):
    if not request.user.is_authenticated:
        return redirect(reverse("user_login"))
    todo = ToDo.objects.get(pk = todo_id)
    context ={
        "todo":todo
    }
    return render(request,"todos/todo_info.html",context)