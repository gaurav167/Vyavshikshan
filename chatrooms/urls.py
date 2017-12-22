#encoding=utf8

from django.urls import path, re_path

from . import views
from .utils.decorators import room_check_access
from .ajax import chat

urlpatterns = [# 'chatrooms',
    # room views
    path('rooms/',
        views.RoomsListView.as_view(),
        name="rooms_list"),
    re_path('room/(?P<slug>[-\w\d]+)/',
        room_check_access(views.RoomView.as_view()),
        name="room_view"),
    path('setguestname/',
        views.GuestNameView.as_view(),
        name="set_guestname"),

    # ajax requests
    path('get_messages/', chat.ChatView().get_messages),
    path('send_message/', chat.ChatView().send_message),
    path('get_latest_msg_id/', chat.ChatView().get_latest_message_id),
    path('get_users_list/', chat.ChatView().get_users_list),
    path('notify_users_list/', chat.ChatView().notify_users_list),
]