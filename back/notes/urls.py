from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet
from django.urls import path
from .views import notes_list, delete_note

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]


urlpatterns = [
    path('notes/', notes_list, name='notes_list'),
    path('notes/delete/<int:note_id>/', delete_note, name='delete_note'),
]