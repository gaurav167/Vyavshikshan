#encoding=utf8

from django.conf.urls import url

from . import views
from .utils.decorators import room_check_access
from .ajax import chat

urlpatterns = [# 'chatrooms',
    # room views
    url('rooms/',
        views.RoomsListView.as_view(),
        name="rooms_list"),
    url('room/(?P<slug>[-\w\d]+)/',
        room_check_access(views.RoomView.as_view()),
        name="room_view"),
    url('setguestname/',
        views.GuestNameView.as_view(),
        name="set_guestname"),

    # ajax requests
    url('get_messages/', chat.ChatView().get_messages),
    url('send_message/', chat.ChatView().send_message),
    url('get_latest_msg_id/', chat.ChatView().get_latest_message_id),
    url('get_users_list/', chat.ChatView().get_users_list),
    url('notify_users_list/', chat.ChatView().notify_users_list),
]