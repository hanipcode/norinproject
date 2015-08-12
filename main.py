import os
import re
import requests
import urllib
import wx
import wx.lib.newevent
import threading
from bs4 import BeautifulSoup 
basedir = os.path.dirname( __file__ )
basedir = os.path.normpath( basedir )
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(basedir , 'requests', 'cacert.pem')
LoggerEvent,EVT_LOGGER = wx.lib.newevent.NewEvent()

    

class Manga_site(object):
	''' This Manga class is for storing a list of Manga website .
		Each website is using different way to store and index their image 
		so we need a different method to crawl from each different site
	'''
	def __init__(self,homepage,collection_page,base_manga_page,manga_title = ""):
		self.manga_title = manga_title.replace(' ','_')
		if not os.path.isdir(self.manga_title):
			os.mkdir(self.manga_title)
		os.chdir(self.manga_title)
		

	@classmethod
	def retrieve_image(self,image_link_list,chapter,win):
		''' download the image '''
		image = urllib.URLopener()
		page_number=1
		chapter = str(chapter)
		for image_link in image_link_list:
			print "trying to download page.... %s" % page_number
			wx.PostEvent(win, LoggerEvent(data1="trying to download page %s .... " % page_number))

			download_to = str(page_number) + ".jpg"
			r = requests.get(image_link,verify=False, stream=True)
			with open(download_to, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						f.flush()
			
			page_number+=1
			wx.PostEvent(win, LoggerEvent(data1="OK! \n" ))
		page_number=1


class Mangacanblog(Manga_site):
	'''
		plugin for mangacanblog.com manga website
	'''
	def __init__(self,manga_title=""):
		homepage = "http://mangacanblog.com"
		collection_page = "http://mangacanblog.com/daftar-komik-manga-bahasa-indonesia.html"
		manga_title = manga_title.lower()
		base_manga_page = "http://mangacanblog.com/baca-komik-%s-bahasa-indonesia-online-terbaru.html" \
		% manga_title.replace(' ','_')
		base_manga_page = base_manga_page.lower()
		Manga_site.__init__(self,homepage,collection_page,base_manga_page,manga_title)
		
	def find_image_url(self,page,current):
			''' search for image url from source code of a page 
			return type = list of URLs
			'''
			print "nyampe find image"
			page_source = BeautifulSoup(requests.get(page).text,"html.parser")
			image_link = page_source.img['src']
			next = int(current) + 1
			next_string = "terbaru-%s" % next
			is_next_page = page_source.body.findAll(text=re.compile(next_string))
			
			if not is_next_page:
				return image_link, None
			else : 
				return image_link, next
	def get_all_image(self,current_chapter,end_chapter,win):
		urllist = []
		current_chapter = int(current_chapter)
		print "nyampe get_all_image"
		next_is_available = True
		while current_chapter <= int(end_chapter):
			wx.PostEvent(win, LoggerEvent(data1="starting download chapter %s \n" % current_chapter))
			page_number = 1
			next_chapter = int(current_chapter) + 1
			if not os.path.isdir(str(current_chapter)):
				os.mkdir(str(current_chapter))
			os.chdir(str(current_chapter))
			while True:
				chapter_link = "http://mangacanblog.com/baca-komik-%s-%s-%s-bahasa-indonesia-%s-%s-terbaru-%s.html" \
				% (self.manga_title.replace(' ','_'),current_chapter,next_chapter, \
				self.manga_title.replace(' ','_'),current_chapter,page_number)
				image_link, next_page = self.find_image_url(chapter_link,page_number)
				urllist.append(image_link)
				wx.PostEvent(win, LoggerEvent(data1="page %s detected \n" % page_number))
				print image_link
				if next_page == None :
					break
				else :
					page_number = next_page
			self.retrieve_image(urllist,current_chapter,win)
			wx.PostEvent(win, LoggerEvent(data1="chapter %s OK! \n" % current_chapter))
			current_chapter += 1
			urllist[:]= []
			os.chdir("../")
		os.chdir("../")			
			
		return urllist