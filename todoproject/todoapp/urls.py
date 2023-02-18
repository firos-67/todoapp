from django.urls import path

from todoapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.TaskListView.as_view(), name='index'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('index/add/', views.add, name='add'),
    path('finish/<int:pk>/', views.finish, name='finish'),
    path('notfinish/<int:pk>/', views.notfinish, name='notfinish'),
    path('cbvdetails/<int:pk>/', views.TaskDetailsView.as_view(), name='cbvdetails'),
    path('cbvedit/<int:pk>/', views.TaskUpdateView.as_view(), name='cbvedit'),
    path('cbvdelete/<int:pk>/', views.TaskDeleteView.as_view(), name='cbvdelete'),
]
