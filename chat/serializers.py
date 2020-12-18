from rest_framework import serializers
from .models import Room, Move, UserRecord


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('code', 'p1', 'p2', 'p1_ready',
                  'p2_ready', 'p1_code', 'p2_code', 'next_move', "first_move")


class UserRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecord
        fields = ('user', 'won', 'total')


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ('room', 'user', 'row', 'col')
