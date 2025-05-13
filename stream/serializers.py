from rest_framework import serializers
from .models import Stream, StreamViewer

class StreamSerializer(serializers.ModelSerializer):
    viewer_count = serializers.SerializerMethodField()
    class Meta:
        model = Stream
        fields = ['id', 'title', 'description', 'is_live', 'created_at', 'stream_key', 'host', 'viewer_count']
        read_only_fields = ['id', 'created_at', 'stream_key']
        
        def get_viewer_count(self, obj):
            return obj.viewers.count()
        
# serializers.py
class StreamViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamViewer
        fields = ['user', 'joined_at']

