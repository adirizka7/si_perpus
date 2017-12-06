from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.http import HttpResponse

def HomePage(request):
    
    # return HttpResponse("metodenya "+request.method+'<br>'+str(request))
    # def post(self,request,**kwargs):
    #     return HttpResponse("metodenya "+request.method)
    print (request)
    # nama_s= request.GET['nama']
    #return HttpResponse("nama anda adalah "+nama_s)
    return render(request, 'index.html',context=None)

    
def atur(request):
    print (request.POST['name'])
    #return render(request, 'hasil.html')
    return HttpResponse("Hai "+request.POST['name']) 