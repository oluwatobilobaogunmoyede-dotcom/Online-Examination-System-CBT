
from django.urls import path
from . import views

urlpatterns = [
    path(
        'examinations/',
        views.available_examinations,
        name='available_examinations'
    ),
    
    path(
    'result/<int:pk>/',
    views.result_detail,
    name='result_detail'
    ),

    path(
        'examinations/start/<int:pk>/',
        views.start_examination,
        name='start_examination'
    ),

    path(
        'take/<int:pk>/',
        views.take_examination,
        name='take_examination'
    ),
]
