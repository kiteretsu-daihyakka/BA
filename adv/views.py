from django.http import Http404
from django.template import loader
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from .models import Publisher

# Create your views here.

def index(request):
    #all_pub = Publisher.objects.all()
    
    #way 1
    #tmp_late = loader.get_template('music/index.html')
    
    #return HttpResponse(tmp_late.render(context, request))
    #context={}
    #way 2
    return redirect('signin:home') #render(request,'adv/AdvPage.html')#,context={'all_albums':all_pub})
    #return HttpResponse(template.render(context,request))
    # html=''
    # all_albums=Album.objects.all()
    # for album in all_albums:
     #   url='music/' + str(album.id) + '/'
     #   html+="<a href='"+ url +"'>"+album.album_title+"</a></br>"
    #return HttpResponse(html)

# def details(request,album_id):
#     try:
#         album = Album.objects.get(pk=album_id)
#     except Album.DoesNotExist:
#         raise Http404('Album does not exist.')
#     #return HttpResponse('<h1>Album details of id : '+str(album_id))4
#     return render(request,'adv/detail.html',{'album':album})

# def adv(request):
#     return render(request,'adv/AdvPage.html')