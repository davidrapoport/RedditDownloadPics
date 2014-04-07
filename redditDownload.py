__author__ = 'David Rapoport'
import requests
import os
from urllib2 import urlopen
import json
import datetime
from PIL import Image
from StringIO import StringIO
import sys
import time
import stat
import subprocess
import wx
from sys import argv

reload(sys)
sys.setdefaultencoding('UTF-8')

def fixCWKD():
	path =os.getcwd()
	path = path[0:3]
	path=path+"Users\\David Rapoport\\Desktop"
	print path
	os.chdir(path)

fixCWKD()
attempts=0
def fixURL(url):
	if url.find(".jpg")>=0:
		while not url[-4:]==".jpg":
			url=url[:-1]
	elif url.find(".gif")>=0:
		while not url[-4:]==".gif":
			url=url[:-1]
	elif url.find(".png")>=0:
		while not url[-4:]==".png":
			url=url[:-1]
	else: url=url+".jpg"
	return url

def fixCaptions(capt):
	capt=capt.replace("\"",'')
	capt=capt.replace(":",'')
	capt=capt.replace("\\",'')
	capt=capt.replace("/",' ')
	capt=capt.replace("?",' ')
	capt=capt.replace("|",' ')
	capt=capt.replace("*",' ')
	capt=capt.replace("<",' ')
	capt=capt.replace(">",' ')
	if(len(capt)>190):capt=capt[:(190-len(capt))]
	return capt

today=datetime.datetime.now()
delta = datetime.timedelta(4)
fourAgo= today-delta
fourString = "Reddit's best for "+str(fourAgo.month) + "_" + str(fourAgo.day) + "_" + str(fourAgo.year)
if os.path.exists(fourString):
	os.chdir(fourString)
	for files in os.listdir("C:\\Users\\David Rapoport\\Desktop\\"+fourString):
		if os.path.isdir(files):
			os.chdir(files)
			for subfiles in os.listdir("C:\\Users\\David Rapoport\\Desktop\\"+fourString+"\\"+files):
				os.remove(subfiles)
			os.chdir("..")
			subprocess.Popen("rmdir " + "\"" + files + "\"", stdout=subprocess.PIPE, shell=True)
		else: os.remove(files)
	os.chdir("..")
	print os.getcwd()
	time.sleep(30)
	subprocess.Popen("rmdir " + "\"" + fourString + "\"", stdout=subprocess.PIPE, shell=True)
	
current =str(today.month) + "_" + str(today.day) + "_" + str(today.year)
current = "Reddit's best for "+ current

print os.getcwd()
if( not os.path.exists(current)): os.makedirs(current,stat.S_IWRITE)
os.chdir(current)
print os.getcwd()
while attempts <=5:
	try:
		passWordFile = open('../redditPassword.txt','r')
		password=passWordFile.read()
		redditUrl= "http://www.reddit.com/.json"
		user_pass_dict ={"api_type": "json", "passwd": password, "rem": True, "user":"drapter4325"}
		#remove quotes from password
#login = requests.post(r"http://www.reddit.com/api/login",data=paramaters)
		session = requests.session()
		session.headers.update({'User-Agent' : 'just doing it for fun \u\drapter4325'})
		login = session.post(r'https://ssl.reddit.com/api/login', data=user_pass_dict)
		loginjson = json.loads(login.content)
		session.modhash=loginjson['json']['data']['modhash']
		urlInfo = session.get(redditUrl)
		urls = list()
		data=urlInfo.json()
		captions=list()
#subprocess.call(["echo","eureka"])


		for children in data['data']['children']:
			test =str(children['data']['url'])
			if test.find('imgur.com')>=0:
				urls.append(test)
				captions.append(str(children['data']['title']))


		j=0
		for pictureURL in urls:
			import urllib
			captions[j]=fixCaptions(captions[j])
			if pictureURL.find("/a/")>=0 and not os.path.exists(captions[j]):
				os.makedirs(captions[j],stat.S_IWRITE)
				os.chdir(captions[j])
				albumText=urllib.urlopen(pictureURL).read()
				album=albumText.split("\n")
				albumURL= list()
				for lines in album:
					if lines.find("View full resolution")>=0:
						albumURL.append("http://" + lines[23:46])
				k=1
				for links in albumURL:
					#print links
					file=open(str(k)+links[-4:],"wb")
					pic= urllib.urlopen(links)
					file.write(pic.read())
					file.close()
					k=k+1
				os.chdir("..")
				j=j+1
				continue

			elif not os.path.exists(captions[j]):
				pictureURL=fixURL(pictureURL)
				print pictureURL
				print captions[j] + pictureURL[-4]
				file=open(captions[j]+pictureURL[-4:],"wb")
				k= urllib.urlopen(pictureURL)
				file.write(k.read())
				file.close()
				j=j+1
			else: j=j+1
		attempts=6
	except Exception as e:
		print str(e)
		attempts= attempts+1
		app=wx.App(False)
		frame = wx.Frame(None, wx.ID_ANY, 'error occured')
		error = wx.MessageDialog(frame, str(e),"ERROR",wx.ICON_ERROR)
		frame.Show(False)
		error.ShowModal()
		time.sleep(30)
