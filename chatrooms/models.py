#encoding=utf8

from django.db import models
from django.contrib.auth.models import User

from polymorphic.models import PolymorphicModel


class Room(PolymorphicModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    description = models.TextField()
    subscribers = models.ManyToManyField(User, blank=True)
    allow_anonymous_access = models.NullBooleanField()
    private = models.NullBooleanField()
    password = models.CharField(max_length=32, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('room_view', [self.slug])
    def __str__(self):
        return self.name


class Message(PolymorphicModel):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # username field is useful to store guest name of unauthenticated users
    username = models.CharField(max_length=20)
    date = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)

    def __str__(self):
        return self.content
