from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess
import os.path
from .models import Log
from .forms import link
import requests
import socket


def openssh(request):
    #  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #    ip = x_forwarded_for.split(',')[0]
    # else:
    #   ip = request.META.get('REMOTE_ADDR')
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    terminal = 'iptables - A INPUT - p tcp -s' + ip + '--dport 22 -j ACCEPT'
    os.system(terminal)
    return HttpResponse("shh finally opened for your ip :" + ip)


def checkme(request):
    # return HttpResponse("working")
    #   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #  if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #    ip = request.META.get('REMOTE_ADDR')
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)

    port22 = subprocess.check_output("nc -zv " + ip + " 22", shell=True)
    port25 = subprocess.check_output("nc -zv " + ip + " 25", shell=True)
    port80 = subprocess.check_output("nc -zv " + ip + " 80", shell=True)
    port443 = subprocess.check_output("nc -zv " + ip + " 443", shell=True)
    if (port22.find("succeeded") != -1):  # check porrt is open
        return HttpResponse("port 22 is open")
    if (port25.find("succeeded") != -1):
        return HttpResponse("port 22 is open")
    if (port80.find("succeeded") != -1):
        return HttpResponse("port 22 is open")
    if (port443.find("succeeded") != -1):
        return HttpResponse("port 22 is open")
    else:
        return HttpResponse("all port is safe")


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
