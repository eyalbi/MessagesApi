from django.contrib import admin
from django.urls import path
from messagesApi import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.api),
    path("login/", views.loginUser,name='login'),
    path("logout/", views.logoutUser),
    path("getusers/",views.getAllUsers),
    path("getMessages/",views.messagesList),
    path("getUnReadMessages/",views.UnreadmessagesList),
    path("readMessage/",views.readMessage),
    path("writeMessage/",views.writeMessage),
    path("deleteMessage/<int:id>",views.deleteMessage)
]
