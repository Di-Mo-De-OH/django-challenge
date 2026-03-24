from django.urls import path

from . import cb_views

app_name = "todo"

urlpatterns = [
    # # FBV
    # path("",views.todo_list,name="todo_list"),
    # path("<int:todo_id>/",views.todo_info,name="todo_info"),
    # path("create/",views.todo_create,name="todo_create"),
    # path("<int:todo_id>/update/",views.todo_update,name="todo_update"),
    # path("<int:todo_id>/delete/",views.todo_delete,name="todo_delete"),
    # CBV
    path("", cb_views.ToDoListView.as_view(), name="list"),
    path("<int:pk>/", cb_views.ToDoDetailView.as_view(), name="info"),
    path("create/", cb_views.ToDoCreateView.as_view(), name="create"),
    path("<int:pk>/update/", cb_views.ToDoUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", cb_views.ToDoDeleteView.as_view(), name="delete"),
    path(
        "comment/<int:todo_id>/create/",
        cb_views.CommentCreateView.as_view(),
        name="create_comment",
    ),
    path(
        "comment/<int:pk>/update/",
        cb_views.CommentUpdateView.as_view(),
        name="update_comment",
    ),
    path(
        "comment/<int:pk>/delete/",
        cb_views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]
