import os
import requests
from bs4 import BeautifulSoup 

class Manga_site:
	''' This Manga class is for storing a list of Manga website .
		Each website is using different way to store and index their image 
		so we need a different method to crawl from each different site
	'''
	def __init__(self,homepage,collection_page,base_manga_page,manga_title = ""):
		self.homepage = homepage
		self.collection_page = collection_page
		self.base_manga_page = base_manga_page
		self.manga_title = manga_title
	
	@classmethod	
	def retrieve_image(image_link,image_path = "",image_name = ""):
		''' download the image '''
		image = urlib.URLopener()
		download_to = imagepath + os.sep + image_name + ".jpg"
		image.retrieve(image_link, download_to )

	def find_image_url(page):
			''' search for image url from source code of a page 
			return type = list of URLs
			'''
			page_source = BeautifulSoup(requests.get(page).text)
			link_found = soup.find_all('a')
			return link_found

class Mangacanblog(Manga_site):
	'''
		plugin for mangacanblog.com manga website
	'''
	def __init__(self,manga_title):
		homepage = "http://mangacanblog.com"
		collection_page = "http://mangacanblog.com/daftar-komik-manga-bahasa-indonesia.html"
		manga_title = manga_title.lower()
		base_manga_page = "http://mangacanblog.com/baca-komik-%s-bahasa-indonesia-online-terbaru.html" \
		% manga_title.replace(' ','_')
		base_manga_page = base_manga_page.lower()
		Manga_site.__init__(self,homepage,collection_page,base_manga_page,manga_title)
	
	def get_current_link(self,current_chapter):
		next_chapter = current_chapter+1
		
		chapter_link = "http://mangacanblog.com/baca-komik-%s-%s-bahasa-indonesia-%s-%s-terbaru-1.html" \
		% (self.manga_title.replace(' ','_'),current_chapter,next_chapter,current_chapter)
		
		print chapter_link;
	def is404(self,link):
		pass
		
manga_name = raw_input('masukan nama seri : ')
manga_chap = raw_input('masukan chapter :')
jmanga= Mangacanblog(manga_name)
print "get manga link...."
manga_chap = jmanga.get_current_link(int(manga_chap))
print "Downloading chapter..."
print "....."