from io import BytesIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to="todo/%Y/%m/%d")
    thumbnail = models.ImageField(
        null=True, blank=True, upload_to="todo/%Y/%m/%d/thumbnail"
    )

    def __str__(self):
        return self.title

    def get_thumbnail_img_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.img:
            return self.img.url
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.img:
            return super().save(*args, **kwargs)

        img = Image.open(self.img)
        img.thumbnail((200, 200))

        img_path = Path(self.img.name)

        thumbnail_name = img_path.stem
        thumbnail_extension = img_path.suffix.lower()

        thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}"

        if thumbnail_extension in [".jpg", ".jpeg"]:
            file_type = "JPEG"
        elif thumbnail_extension == ".png":
            file_type = "PNG"
        elif thumbnail_extension == ".gif":
            file_type = "GIF"
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        img.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "todo"
        verbose_name_plural = "todo 목록"


class Comment(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "댓글목록"
