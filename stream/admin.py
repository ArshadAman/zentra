from django.contrib import admin
from .models import CameraAngle,Stream,StreamViewer

# Register your models here.
admin.site.register(CameraAngle)
admin.site.register(Stream)
admin.site.register(StreamViewer)

