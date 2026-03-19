from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class ToDo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name = "todo"
        verbose_name_plural = "todo 목록"


