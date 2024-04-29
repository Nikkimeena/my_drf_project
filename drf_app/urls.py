from django.urls import path
from drf_app import views


# from rest_framework.routers import DefaultRouter

# router=DefaultRouter()


# router.register('bookapi',views.BookViewset,basename='book')


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
    path('Detail/<int:pk>/',views.Detail.as_view()),
    path('BookList/',views.BookList.as_view(),name='BookList'),
    path('BookCreate/',views.BookCreate.as_view(),name='BookCreate'),
    path('BookRetrieve/<int:pk>/',views.BookRetreive.as_view(),name='BookRetrieve'),
    path('BookUpdate/<int:pk>/',views.BookUpdate.as_view(),name='BookUpdate'),
    path('BookDelete/<int:pk>/',views.BookDelete.as_view(),name='BookDelete'),
    path('BookListCreate/',views.BookListCreate.as_view()),
    path('BookRetrieveUpdate/<int:pk>/',views.BookRetrieveUpdate.as_view()),
    path('Book_delete/<int:pk>/',views.Book_delete.as_view()),
    path('Book_update_delete/<int:pk>/',views.Book_update_delete.as_view()),
    
 
]