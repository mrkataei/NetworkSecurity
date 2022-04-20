import os
import requests
import socket
import subprocess
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from . import models
from . import serializers


def create_log(request, operation):
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    system = request.META.get('HTTP_USER_AGENT')
    models.Log(ip=ip, system=system, operation=operation).save()
    return ip


@api_view(['GET'])
def domain(request):
    ip = create_log(request, 'domain')
    return Response({'result': "your ip : " + ip}, status.HTTP_200_OK)


@api_view(['GET'])
def openssh(request):
    # open port 22 for client
    try:
        ip = create_log(request, 'ssh')
        terminal = 'iptables - A INPUT - p tcp -s' + ip + '--dport 22 -j ACCEPT'
        os.system(terminal)
        return Response({'message': "shh finally opened for your ip :" + ip}, status.HTTP_200_OK)
    except:
        return Response({'error': "something wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_me(request):
    # check client open ports
    try:
        ip = create_log(request, 'check')
        port = request.data["port"]
    except:
        return Response({'error': "send your request port"}, status.HTTP_400_BAD_REQUEST)
    else:
        if isinstance(port, int):
            result = subprocess.check_output("nc -zv " + ip + str(port), shell=True)
            if str(result).find("succeeded") != -1:  # port is open
                return Response({'result': f"port {port} is open :" + ip}, status.HTTP_200_OK)
        else:
            return Response({'error': "send integer values"}, status.HTTP_400_BAD_REQUEST)


class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer
    http_method_names = ['get']
    search_fields = ('name',)
    ordering_fields = ('date',)

    def list(self, request, *args, **kwargs):
        objs = super().list(request, *args, **kwargs)
        create_log(request, 'logs')
        print("---- List ----")
        return objs

    # def create(self, request, *args, **kwargs):
    #     obj = super().create(request, *args, **kwargs)
    #     print("---- Create ----")
    #     return obj

    # def update(self, request, *args, **kwargs):
    #     obj = super().update(request, *args, **kwargs)
    #     instance = self.get_object()
    #     print("---- Update : {}".format(instance.name))
    #     return obj

    def retrieve(self, request, *args, **kwargs):
        obj = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        print("---- Retrieve : {}".format(instance.name))
        return obj

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print("---- Destroy : {}".format(instance.name))
    #     obj = super().destroy(request, *args, **kwargs)
    #     return obj

    # def get_serializer_class(self):
    #     if self.request.method not in permissions.SAFE_METHODS:
    #         return serializers.Log
    #     else:
    #         return serializers.LogReadSerializer


@api_view(['GET'])
def get_log(request):
    logs = models.Log.objects.all()
    ser = serializers.LogSerializer(logs, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ddos(request):
    ip = create_log(request, 'ddos')
    terminal = 'iptables -A INPUT -s ' + ip + ' -j DROP'
    BASE = os.path.dirname(os.path.abspath(__file__))
    # firstRange=ip.split(".")[0]
    # SecondRange = ip.split(".")[1]
    # ThirdRange = ip.split(".")[2]
    # FourthRange = ip.split(".")[3]
    # ip='185.1.172.0'
    try:
        # ip="185.172.68.0"
        with open(os.path.join(BASE, "static/api/iran_ip.txt")) as f:
            is_iran = True if ip in f.read() else False
        if not is_iran:
            os.system(terminal)
            return Response({'result': "your ip is banned"}, status.HTTP_200_OK)
        else:
            return Response({'result': "welcome Iran"}, status.HTTP_200_OK)
    except:
        return Response({'error': "something wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkAvailability(request):
    # check client open ports
    try:
        create_log(request, 'available')
        link = request.data["link"]
    except:
        return Response({'error': "send your request link"}, status.HTTP_400_BAD_REQUEST)
    else:
        req = requests.get(link)
        http = req.status_code
        result = "open" if http == 200 else "close"
        return Response({'result': f"website is  {result}"}, status.HTTP_200_OK)


@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes((permissions.IsAdminUser, ))
def get_update_delete_white_ip(request, pk):
    try:
        ip = models.WhiteIP.objects.get(pk=pk)
    except:
        return Response({"error": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = serializers.WhiteIPSerializer(ip)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        ser = serializers.WhiteIPSerializer(ip, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((permissions.IsAdminUser, ))
def post_white_ip(request):
    data = {
        'ip': request.data['ip'],
        'country': request.data['country'],
    }

    ser = serializers.WhiteIPSerializer(data=data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_ip(request):
    ip = models.WhiteIP.objects.filter(name=request.query_params['ip'])
    if ip:
        ser = serializers.WhiteIPSerializer(ip, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_white_ips(request):
    ips = models.WhiteIP.objects.all()
    ser = serializers.WhiteIPSerializer(ips, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)
