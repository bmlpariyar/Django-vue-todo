from django.db import models
from django.contrib.auth.models import User

class Todo_List(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  completed =  models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ['-created_at', '-updated_at']

  def __str__(self):
    return self.title