#!/usr/bin/env python
import subprocess
import csv
import os
import sys
import time
from os import listdir
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
from main.models import Video
import django
from os.path import isfile, join
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG_BIN = "ffmpeg" 
import subprocess as sp

videolist = [f for f in listdir('%s/media/uploads/pre/' % BASE_DIR) if isfile(join('%s/media/uploads/pre/' % BASE_DIR, f))]

print videolist

for video in videolist:
	# time.sleep(5)

	file_string = "%s" % video

	print file_string

	try:
		filename, file_extension = os.path.splitext(file_string)
		os.rename('%s/media/uploads/pre/%s' % (BASE_DIR,video) ,'%s/media/uploads/convert/%s' % (BASE_DIR,video))

		
		if not file_extension == '.mp4':
			subprocess.call(['ffmpeg', '-i', '%s/media/uploads/convert/%s' % (BASE_DIR,video), '%s/media/uploads/done/%s.mp4' % (BASE_DIR,video[0:len(video)-4])])
			# command = [ FFMPEG_BIN,
			# 			'-i', '%s/media/uploads/convert/%s' % (BASE_DIR,video),
			# 			'%s/media/uploads/done/%s.mp4' % (BASE_DIR,video[0:len(video)-4])]

			

			# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
			# sp.Pclose()
			# time.sleep(5)
			# pipe.kill()
			os.remove('%s/media/uploads/convert/%s' % (BASE_DIR,video))
			print "1@@@@@@@@@@@@@@@@"
			print "1@@@@@@@@@@@@@@@@"
			print "1@@@@@@@@@@@@@@@@"
			vidname = video[0:len(video)-4]
			print vidname
			print "2@@@@@@@@@@@@@@@@"
			print "2@@@@@@@@@@@@@@@@"
			print "2@@@@@@@@@@@@@@@@"
			savedvid = Video.objects.get(stamp=vidname)

			print "3@@@@@@@@@@@@@@@@"
			print "3@@@@@@@@@@@@@@@@"
			print "3@@@@@@@@@@@@@@@@"
			savedvid.done = True
			savedvid.save()




			
		else:
			os.rename('%s/media/uploads/convert/%s' % (BASE_DIR,video) ,'%s/media/uploads/done/%s' % (BASE_DIR,video))
			vidname = video[0:len(video)-3]
			savedvid = Video.objects.get(stamp=vidname)
			savedvid.done = True
			savedvid.save()


		# os.rename('%s/media/uploads/convert/%s' % (BASE_DIR,video) ,'%s/media/uploads/done/%s' % (BASE_DIR,video))
	except Exception, e:
		print e




