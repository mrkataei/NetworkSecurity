from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess
import os.path
from .models import Log
from .forms import link
import requests
import socket
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def openssh(request):
    # open port 22 for client
    try:
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name)
        terminal = 'iptables - A INPUT - p tcp -s' + ip + '--dport 22 -j ACCEPT'
        os.system(terminal)
        return Response({'message': "shh finally opened for your ip :" + ip}, status.HTTP_200_OK)
    except:
        return Response({'error': "something wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_me(request):
    # check client open ports
    try:
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name)
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


def log(request):
    #  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #    ipAdd = x_forwarded_for.split(',')[0]
    # else:
    # ipAdd = request.META.get('REMOTE_ADDR')
    host_name = socket.gethostname()
    ipAdd = socket.gethostbyname(host_name)

    #  headers = request.utils.default_headers()
    user = request.META.get('HTTP_USER_AGENT')  # get user agent

    log = Log(
        user_agent=user,
        ip=ipAdd,

    )
    log.save()

    # user_A=log.user_agent
    # ip_t=log.ip
    return HttpResponse(log.FinishTime)


def ddos(request):
    #   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #    if x_forwarded_for:
    #       ip = x_forwarded_for.split(',')[0]
    #  else:
    #     ip = request.META.get('REMOTE_ADDR')
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    # firstRange=ip.split(".")[0]
    # SecondRange = ip.split(".")[1]
    # ThirdRange = ip.split(".")[2]
    # FourthRange = ip.split(".")[3]
    # ip='185.1.172.0'
    is_iran = False
    terminal = 'iptables -A INPUT -s ' + ip + ' -j DROP'
    BASE = os.path.dirname(os.path.abspath(__file__))
    # ip="185.172.68.0"
    with open(os.path.join(BASE, "iranip.txt")) as f:
        if ip in f.read():
            is_iran = True
    if not (is_iran):
        os.system(terminal)
        return HttpResponse(ip)
    else:
        return HttpResponse("welcomme iruni")


def checkAvailability(request):
    form = link(request.POST)
    if form.is_valid():
        text = form.cleaned_data['linkget']
    else:
        text = 'http://vu.um.ac.ir'
    # hhtp=httplib2.HTTPConnectionWithTimeout(text).getresponse().status
    # https=httplib2.HTTPSConnectionWithTimeout(text).getresponse().status

    # h=urlopen(text)
    # t=h.getcode()
    req = requests.get(text)
    http = req.status_code
    if (http == 200):
        res = "is open"
    else:
        res = "is close"
    args = {'form': form, 'text': res, 'matn': text}
    return render(request, 'form.html', args)


def domin(request):
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    return HttpResponse(ip)
