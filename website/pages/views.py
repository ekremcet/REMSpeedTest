from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.cache import never_cache
import requests, time, datetime
import pages.Client as Client
@never_cache
def home(request):
    compress = False
    if (request.POST.get('mybtn3')):
        client = Client.Client('13.80.2.211', 33333)
        
        #get ping:
        client.connect_to_server()
        latency = client.ping_test()
        #get download
        client.connect_to_server()
        download = client.download_test()
        #get upload
        client.connect_to_server()
        upload = client.upload_test()
        # close connection
        client.server_sock.close()
       
        print("LATENCY: {}\nDOWNLOAD: {}\nUPLOAD: {}".format(latency, download, upload))
        
        return render(request, 'home.html', {"latency": latency, "download": download, "upload": upload})

    else:
        return render(request, 'home.html', {"latency": "", "download": "", "upload": ""})




