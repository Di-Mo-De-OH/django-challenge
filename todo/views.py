from django.shortcuts import render,redirect
from django.urls import reverse
from todo.models import ToDo
from django.contrib.auth.decorators import login_required
from todo.forms import ToDoForm,TodoUpdateForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
@login_required()
def todo_list(request):
    
    todos = ToDo.objects.filter(user=request.user).order_by("-created_at")
    q=request.GET.get("q")
    if q:
        todos = todos.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    page = request.GET.get("page",1)
    paginator = Paginator(todos,10)
    page_obj = paginator.get_page(page)



    context = {
        "todos":todos,
        "page_obj":page_obj,
        "q":q
    }
    return render(request,"todos/todo_list.html",context)









@login_required()
def todo_info(request,todo_id):
    todo = get_object_or_404(ToDo,pk = todo_id)
    if todo.user != request.user:
        return redirect(reverse("todo_list"))
    context ={
        "todo":todo
    }
    return render(request,"todos/todo_info.html",context)

@login_required()
def todo_create(request):
    form = ToDoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
    
        return redirect(reverse("todo_info",kwargs={"todo_id":todo.id}))
    context = {"form":form}
    return render(request,"todos/todo_create.html",context)
    

@login_required()
def todo_update(request,todo_id):
    todo = get_object_or_404(ToDo,pk =todo_id,user = request.user)
    form = TodoUpdateForm(request.POST or None,instance = todo)
    if form.is_valid():
        todo = form.save()
        return redirect(reverse("todo_info",kwargs={"todo_id":todo.id}))
    context = {
        "form":form
    }
    return render(request,"todos/todo_update.html",context)

@login_required()
def todo_delete(request,todo_id):
    todo = get_object_or_404(ToDo,pk =todo_id,user = request.user)
    todo.delete()
    return redirect(reverse("todo_list"))

