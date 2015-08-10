import os
import re
import requests
import urllib
from bs4 import BeautifulSoup 

http_proxy  = "http://192.168.137.2:8118"
https_proxy = "http://192.168.137.2:8118"
ftp_proxy   = "http://192.168.137.2:8118"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }
			
class Manga_site(object):
	''' This Manga class is for storing a list of Manga website .
		Each website is using different way to store and index their image 
		so we need a different method to crawl from each different site
	'''
	def __init__(self,homepage,collection_page,base_manga_page,manga_title = ""):
		self.manga_title = manga_title.replace(' ','_')
		if not os.path.isdir(self.manga_title):
			os.mkdir(self.manga_title)

	@classmethod
	def retrieve_image(self,image_link_list,chapter):
		''' download the image '''
		image = urllib.URLopener(proxies=proxyDict)
		page_number=1
		chapter = str(chapter)
		for image_link in image_link_list:
			print "trying to download page.... %s" % page_number
			download_to = str(page_number) + ".jpg"
			r = requests.get(image_link, stream=True,proxies=proxyDict)
			with open(download_to, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						f.flush()
			page_number+=1


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
		
	def find_image_url(self,page,current):
			''' search for image url from source code of a page 
			return type = list of URLs
			'''
			page_source = BeautifulSoup(requests.get(page,proxies=proxyDict).text)
			image_link = page_source.img['src']
			next = int(current) + 1
			next_string = "terbaru-%s" % next
			is_next_page = page_source.body.findAll(text=re.compile(next_string))
			
			if not is_next_page:
				return image_link, None
			else : 
				return image_link, next
	def get_all_image(self,current_chapter,end_chapter):
		os.chdir(self.manga_title)
		urllist = []
		page_number = 1
		current_chapter = int(current_chapter)
		next_is_available = True
		while current_chapter <= int(end_chapter):
			next_chapter = current_chapter + 1
			if not os.path.isdir(str(current_chapter)):
				os.mkdir(str(current_chapter))
			os.chdir(str(current_chapter))
			while True:
				chapter_link = "http://mangacanblog.com/baca-komik-%s-%s-%s-bahasa-indonesia-%s-%s-terbaru-%s.html" \
				% (self.manga_title.replace(' ','_'),current_chapter,next_chapter, \
				self.manga_title.replace(' ','_'),current_chapter,page_number)
				image_link, next_page = self.find_image_url(chapter_link,page_number)
				urllist.append(image_link)
				
				if next_page == None :
					break
				else :
					page_number = next_page
			self.retrieve_image(urllist,current_chapter)
			current_chapter += 1
			os.chdir("../")
					
			
		return urllist
		
		
		
manga_name = raw_input('masukan nama seri : ')
manga_chap = raw_input('masukan chapter :')
manga_chapend = raw_input('mau download sampe chater berapa? :')
jmanga= Mangacanblog(manga_name)
print "get manga link...."
print jmanga.get_all_image(manga_chap,manga_chapend)