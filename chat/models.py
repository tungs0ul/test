from django.db import models
from django.contrib.auth import get_user_model
import string
import random
# Create your models here.


User = get_user_model()


def generate_random_code(length=5):
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if not Room.objects.all().filter(code=code):
            return code


class Room(models.Model):
    code = models.SlugField(unique=True)
    p1 = models.CharField(null=True, blank=True, max_length=50)
    p2 = models.CharField(null=True, blank=True, max_length=50)
    p1_code = models.CharField(null=True, blank=True, max_length=255)
    p2_code = models.CharField(null=True, blank=True, max_length=255)
    p1_uid = models.IntegerField(null=True, blank=True)
    p2_uid = models.IntegerField(null=True, blank=True)
    p1_ready = models.BooleanField(default=False)
    p2_ready = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    next_move = models.CharField(default="p1", max_length=2)
    first_move = models.CharField(default="p1", max_length=2)

    def __str__(self):
        return self.code


class Move(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.CharField(max_length=2)
    row = models.IntegerField()
    col = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['room', 'row', 'col']

    def __str__(self) -> str:
        return str(self.user) + str(self.room) + "row: " + str(self.row) + " col: " + str(self.col) + str(self.createdAt)


class UserRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    won = models.IntegerField()
    total = models.IntegerField()

    def __str__(self) -> str:
        return str(self.user) + str(self.won) + " / " + str(self.total)
