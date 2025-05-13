from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import Stream, StreamViewer
from .serializers import StreamSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class StreamListCreateView(generics.ListCreateAPIView):
    queryset = Stream.objects.all().order_by('-created_at')
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class StreamDetailView(generics.RetrieveDestroyAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        stream = self.get_object()
        if stream.host != request.user:
            return Response({"error": "You can't delete this stream."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
class StartStreamView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        stream = Stream.objects.get(pk = pk)
        if stream.host != request.user:
            return Response({"error": "You can't start this stream."}, status=status.HTTP_403_FORBIDDEN)
        stream.is_live = True
        stream.save()
        return Response({"message": "Stream started successfully."}, status=status.HTTP_200_OK)
    

class JoinStreamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        stream = get_object_or_404(Stream, pk=pk)

        if not stream.is_live:
            return Response({'detail': 'Stream is not live yet.'}, status=status.HTTP_400_BAD_REQUEST)

        viewer, created = StreamViewer.objects.get_or_create(stream=stream, user=request.user)

        if not created:
            return Response({'detail': 'You have already joined this stream.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Joined stream successfully.'}, status=status.HTTP_201_CREATED)
    
class EndStreamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        stream = get_object_or_404(Stream, pk=pk)

        if stream.host != request.user:
            return Response({'detail': 'You are not the host of this stream.'}, status=status.HTTP_403_FORBIDDEN)
        
        if stream.is_live == False:
                return Response({"detail": "Stream already ended."}, status=status.HTTP_400_BAD_REQUEST)

        stream.end_stream()
        return Response({'detail': 'Stream ended successfully.'}, status=status.HTTP_200_OK)


class LeaveStreamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, stream_id):
        try:
            stream = Stream.objects.get(id=stream_id)
            
            # Check if the user is already watching the stream
            viewer = StreamViewer.objects.filter(stream=stream, user=request.user).first()
            
            if not viewer:
                return Response({"detail": "You are not a viewer of this stream."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Remove the viewer from the stream
            viewer.delete()
            
            return Response({"detail": "You have left the stream."}, status=status.HTTP_200_OK)
        
        except Stream.DoesNotExist:
            return Response({"detail": "Stream not found."}, status=status.HTTP_404_NOT_FOUND)