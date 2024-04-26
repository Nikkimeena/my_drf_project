from django.urls import path
from drf_app import views

urlpatterns = [
    path('user_list/', views.user_list),
    path('hello_world/', views.hello_world),
    path('user-api/',views.user_api),
    path('add-user/',views.add_user),
    path('update-user/<int:id>/',views.update_user),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('user-list/',views.UserList.as_view()),
    path('User-detail/<int:pk>/',views.UserDetail.as_view()),
    path('alluserlist/',views.AllUserList.as_view()),
    path('userinfo/<int:pk>/',views.UserInfo.as_view()),
    path('List/',views.List.as_view()),
    path('Detail/<int:pk>/',views.Detail.as_view())
]