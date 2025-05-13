from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
# Create your models here.
class Stream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_live = models.BooleanField(default=False)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streams')
    stream_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def end_stream(self):
        self.is_live = False
        self.end_time = timezone.now()
        self.save()
        
        return self
    
class StreamViewer(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='viewers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('stream', 'user')  # Prevent duplicate joins
        