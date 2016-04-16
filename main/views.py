from django.shortcuts import render
import subprocess

from forms import VideoUpload
from main.models import Video, CustomUser
from datetime import datetime
import time
from forms import SignUpForm, LoginForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



# Create your views here.

# def convert(request):
# 	subprocess.call('ffmpeg -i video.flv video.mp4')
# 	return HttpResponse('DONE !')


import subprocess as sp
FFMPEG_BIN = "ffmpeg" 

def myvideos(request):
	context = {}
	videos = Video.objects.filter(user=request.user)

	context['videos'] = videos

	return render(request ,'videolist.html' ,context)



def displayvideo(request, pk):
	context = {}

	video = Video.objects.get(pk=pk)

	video.count += 1

	video.save()

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
				command = [ FFMPEG_BIN,
		            		'-i', 'media/%s' % video.file,
		            		'media/uploads/%s.mp4' % video.stamp]
				pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
				savedvid.file = "uploads/%s.mp4" % timestring
				savedvid.save()
				

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
				return redirect('/case_list/')
			except Exception, e:
				return HttpResponse('invalid user, try again <a htrf="/login/">here</a>')
	return render(request, 'login.html', context)

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
			except Exception, e:
				return HttpResponse('invalid user, try again <a htrf="/signup/">here</a>')

	return render(request, 'signup.html', context)