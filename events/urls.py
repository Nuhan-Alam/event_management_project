from django.contrib import admin
from django.urls import path,include
from events.views import home,participants,categories,create_event,dashboard,create_cate,add_people,event_details,successful,update_event,delete_event,update_cate,delete_cate,update_people,delete_people,search_events
# from users import views
# from users.views import user_dashboard,task_create,view_task,manager_dashboard;

urlpatterns = [
    path('home/', home,name='home'),
    path('serach/', search_events,name='search'),
    path('event_details/<int:event_id>/', event_details,name='event_details'),
    path('participants/', participants,name='participants'),
    path('categories/', categories,name='categories'),


    path('create_event/', create_event,name='create_event'),
    path('update_event/<int:id>/', update_event, name='update_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'),


    path('create_category/', create_cate,name='create_cate'),
    path('update_category/<int:id>/', update_cate,name='update_cate'),
    path('delete_category/<int:id>/', delete_cate,name='delete_cate'),



    path('add_participants/', add_people,name='add_people'),
    path('update_partcipants/<int:id>/', update_people,name='update_people'),
    path('delete_partcipants/<int:id>/', delete_people,name='delete_people'),



    path('dashboard/', dashboard,name='dashboard'),
    path('successful/', successful ,name='successful'),
    # path('manager_dashboard/', manager_dashboard,name="manager-dashboard"),
    # path('create_task/',task_create),
    # path('view_task/', view_task)
]
