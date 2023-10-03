from django.urls import path
from .views import TodoView, TodoDetailView, TodoDoneView, TodoDetailDoneView

urlpatterns = [
    path('todo/', TodoView.as_view(), name='todo_view'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='todo_detail_view'),
    path('done/', TodoDoneView.as_view(), name='todo_done_view'),
    path('done/<int:pk>/', TodoDetailDoneView.as_view()),

]
