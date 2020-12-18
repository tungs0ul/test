import json
from django.shortcuts import render
from .models import Room, Move, UserRecord, generate_random_code
from .serializers import RoomSerializer, MoveSerializer, UserRecordSerializer
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response

# Create your views here.


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


num = 0


def login(request):
    global num
    num += 1
    data = {'num': num}
    return JsonResponse(data)


def finish(request):
    room = Room.objects.get(code=request.data['room'].upper())
    moves = Move.objects.filter(room=room)
    for move in moves:
        move.delete()
    room.first_move = "p1" if room.first_move == "p2" else "p2"
    return JsonResponse({'msg': 'ok'})


class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, format='None'):
        if request.query_params['mode'] == 'all':
            rooms = self.queryset.order_by('-createdAt')
            serializer = RoomSerializer(rooms, many=True)
            return Response(serializer.data)
        elif request.query_params['mode'] == 'info':
            print(request.query_params)
            room = self.queryset.get(code=request.query_params['room'])
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        else:
            return JsonResponse({'msg': 'failed'})

    def post(self, request, format='None'):
        if request.data['mode'] == 'join':
            try:
                room = self.queryset.get(code=request.data['room'])
                if room.p1 and room.p2:
                    return JsonResponse({'msg': 'inspect'})
                elif not room.p1:
                    room.p1 = request.data['user']
                    room.p1_uid = request.data['uid']
                    room.save()
                    return JsonResponse({'msg': 'p1'})
                elif not room.p2:
                    room.p2 = request.data['user']
                    room.p2_uid = request.data['uid']
                    room.save()
                    return JsonResponse({'msg': 'p2'})
            except:
                return JsonResponse({'msg': 'failed'})
        elif request.data['mode'] == 'host':
            room = Room(code=generate_random_code(),
                        p1=request.data['user'], p1_uid=int(request.data['uid']))
            room.save()
            return JsonResponse({'msg': 'p1', 'lobby': room.code})
        elif request.data['mode'] == 'ready':
            room = self.queryset.get(code=request.data['room'])
            if request.data['player'] == "p1":
                room.p1_ready = True
            elif request.data['player'] == "p2":
                room.p2_ready = True
            room.save()
            return JsonResponse({"msg": "ok"})
        elif request.data['mode'] == 'exit':
            room = self.queryset.get(code=request.data['room'])
            if request.data['uid'] == room.p1_uid:
                room.p1 = None
                room.p1_code = None
                room.p1_uid = None
                room.p1_ready = False
                room.save()
            elif request.data['uid'] == room.p2_uid:
                room.p2 = None
                room.p2_code = None
                room.p2_uid = None
                room.p2_ready = False
                room.save()
            if not (room.p1_code or room.p2_code):
                room.delete()
            return JsonResponse({'msg': 'exit'})


class MoveView(generics.CreateAPIView):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer

    def get(self, request, format='None'):
        room = Room.objects.get(code=request.query_params['room'].upper())
        moves = self.queryset.filter(room=room).order_by('createdAt')
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data)

    def post(self, request, format="None"):
        try:
            room = Room.objects.get(code=request.data['room'])
            move = Move(room=room, user=request.data['user'],
                        row=request.data['row'], col=request.data['col'])
            room.next_move = "p1" if room.next_move == "p2" else "p1"
            move.save()
            return JsonResponse({'msg': 'ok'})
        except:
            return JsonResponse({"msg": 'failed'})


class UserRecordView(generics.CreateAPIView):
    queryset = UserRecord.objects.all()
    serializer_class = UserRecordSerializer
