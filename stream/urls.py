from django.urls import path,include
from .views import StreamListCreateView, StreamDetailView, StartStreamView, JoinStreamView, EndStreamView, LeaveStreamView
from rest_framework.routers import DefaultRouter
from .views import CameraAngleView



router = DefaultRouter()
router.register(r'cameraangle',CameraAngleView)


urlpatterns = [
    path('streams/', StreamListCreateView.as_view(), name='stream_list_create'),
    path('streams/<int:pk>/', StreamDetailView.as_view(), name='stream_detail'),
    path('streams/<int:pk>/start/', StartStreamView.as_view(), name='start-stream'),
     # urls.py
    path('streams/<int:pk>/join/', JoinStreamView.as_view(), name='join-stream'),
    path('end_stream/<int:stream_id>/', EndStreamView.as_view(), name='end_stream'),
    path('leave_stream/<int:stream_id>/', LeaveStreamView.as_view(), name='leave_stream'),
    path('',include(router.urls)),
]
