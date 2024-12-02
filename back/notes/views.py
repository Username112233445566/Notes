# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from django.db.models import Q

class NoteListCreateAPIView(APIView):
    def get(self, request):
        notes = Note.objects.all()
        sort_by = request.query_params.get('sort_by', 'created_at')
        filter_query = request.query_params.get('filter', None)

        if filter_query:
            notes = notes.filter(Q(title__icontains=filter_query) | Q(content__icontains=filter_query))
        notes = notes.order_by(sort_by)
        
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
