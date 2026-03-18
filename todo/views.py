from django.shortcuts import render
from todo.models import ToDo
# Create your views here.

def todo_list(request):
    todos = ToDo.objects.filter()
    context = {
        "todos":todos
    }
    return render(request,"todo_list.html",context)

def todo_info(request,todo_id):
    todo = ToDo.objects.get(pk = todo_id)
    context ={
        "todo":todo
    }
    return render(request,"todo_info.html",context)