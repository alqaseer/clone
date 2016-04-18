from django.shortcuts import render, redirect
import subprocess

from forms import VideoUpload
from main.models import Video, CustomUser
from datetime import datetime
import time
from forms import SignUpForm, LoginForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

import os

# Create your views here.

# def convert(request):
#   subprocess.call('ffmpeg -i video.flv video.mp4')
#   return HttpResponse('DONE !')


import subprocess as sp
FFMPEG_BIN = "ffmpeg" 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def myvideos(request):
    context = {}
    videos = Video.objects.filter(user=request.user)

    context['videos'] = videos

    return render(request ,'videolist.html' ,context)



def displayvideo(request, pk):

    video = Video.objects.get(pk=pk)
    print "count before: %s" % video.count
    video.count += 1
    print "count after: %s" % video.count
    video.save()

    context = {}

    context['video'] = video

    return render(request, 'video.html', context)

def convert(request):
    command = [ FFMPEG_BIN,
                '-i', 'video.flv',
                'video.mp4']
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    return HttpResponse('done !')


def upload(request):
    if request.user.is_active:

        context = {}

        context['form'] = VideoUpload()


        if request.method == 'POST':
            
            form = VideoUpload(request.POST, request.FILES)
            context['form'] = form
            if form.is_valid():
                video = form.save(commit=False)
                currentdate = datetime.now()
                timestring = currentdate.strftime("%Y%m%d%H%M%S")
                video.stamp = timestring
                video.user = request.user
                video.save()
                
                
                
                savedvid = Video.objects.get(stamp=timestring)
                namenoext = '%s' % savedvid.file
                ext = namenoext[len(namenoext)-3:len(namenoext)]
                os.rename('%s/media/%s' % (BASE_DIR,savedvid.file) ,'%s/media/uploads/pre/%s.%s' % (BASE_DIR,timestring,ext))
                savedvid.file = "uploads/done/%s.mp4" % timestring
                savedvid.save()

                # # vid_check = str(video.file[len(video.file)-3:len(video.file)])

                # file_string = "%s" % video.file

                # filename, file_extension = os.path.splitext(file_string)

                # print '------'
                # print 'file string:: %s' % file_extension
                # print '------'
                # print 'file extension %s' % file_extension

                # if not file_extension == '.mp4':
                #     subprocess.call(['ffmpeg', '-i', 'media/%s' % video.file, 'media/uploads/%s.mp4' % video.stamp])
                #     # command = [ FFMPEG_BIN,
                #     #             '-i', 'media/%s' % video.file,
                #     #             'media/uploads/%s.mp4' % video.stamp]
                #     # pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
                    
                #     savedvid.file = "uploads/%s.mp4" % timestring
                #     savedvid.save()


                return redirect('/myvideos/')
                

        return render(request, 'upload.html', context)
    else:
        return HttpResponse('You are Still not an active user , please wait will activate you soon')




#user managment views
def logout_view(request):
    logout(request)
    return redirect('/signup/')

def login_view(request):

    context = {}

    context['form'] = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email', None)
            password = form.cleaned_data.get('password', None)

            auth_user = authenticate(username=email, password=password)

            try:
                login(request, auth_user)
                return redirect('/myvideos/')
            except Exception, e:
                return HttpResponse('invalid user, try again <a htrf="/login/">here</a>')
    return render(request, 'login.html', context)
def deletevid(request, pk):
    video = Video.objects.get(pk=pk)
    video.delete()
    return HttpResponse('DELETED !')




def signup(request):

    context = {}

    context['form'] = SignUpForm()

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        context['form'] = form

        if form.is_valid():

            form.save()

            email = form.cleaned_data.get('email', None)
            password = form.cleaned_data.get('password1', None)

            auth_user = authenticate(username=email, password=password)

            try:
                login(request, auth_user)
                return redirect('/myvidoes/')
            except Exception, e:
                return HttpResponse('invalid user, try again <a htrf="/signup/">here</a>')

    return render(request, 'signup.html', context)