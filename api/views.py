import os
import requests
import socket
import subprocess
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models


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


@api_view(['GET'])
def log(request):
    # response client his logs
    ip = create_log(request, 'logs')
    try:
        logs = models.Log.objects.filter(ip=ip).values("ip", "operation",
                                                       "system", "date")
        return Response({'result': logs}, status.HTTP_200_OK)
    except:
        return Response({'error': "something wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
