from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Note
from .serializers import NoteSerializer
from django.shortcuts import render


class NoteListView(APIView):
    """
    API для отображения списка заметок и создания новой заметки.
    """
    def get(self, request):
        notes = Note.objects.all().order_by('-created_at')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
    """
    API для редактирования и удаления заметки.
    """
    def get_object(self, pk):
        return get_object_or_404(Note, pk=pk)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Вспомогательные HTML представления
def notes_list(request):
    """
    HTML-страница для работы с заметками.
    """
    if request.method == 'POST':
        note_id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if note_id:
            note = get_object_or_404(Note, id=note_id)
            note.title = title
            note.content = content
            note.save()
        else:
            Note.objects.create(title=title, content=content)

        return HttpResponseRedirect('/notes/')

    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes_list.html', {'notes': notes})


def delete_note(request, note_id):
    """
    Удаление заметки через HTML.
    """
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return HttpResponseRedirect('/notes/')
