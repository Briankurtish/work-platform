from django.urls import path
from .views import TasksView



urlpatterns = [
    
    path(
        "task-panel/",
        TasksView.as_view(template_name="tasks.html"),
        name="task-panel",
    )
]
