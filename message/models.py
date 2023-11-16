from django.db import models


class Message(models.Model):  # 모델은 메세지라고 가칭 지어놓음.
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = "messages"
