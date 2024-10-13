from django.db import models

# Create your models here.
class Document(models.Model):
    
    content = models.TextField()
    
    def __str__(self):
        return self.content[:20]
