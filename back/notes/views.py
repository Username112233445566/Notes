from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Note
from .serializers import NoteSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['created_at']
    ordering_fields = ['created_at']

def notes_list(request):
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

        return redirect('notes_list')

    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes_list.html', {'notes': notes})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('notes_list')