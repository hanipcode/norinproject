GUIDELINES:

@name = jManga
@lang = python
@author = Muhammad Hanif

Question of v.0.1 : 
What your program is? 
	A software that can download a volume of manga from spesific manga website
How?
	1. Input the link of initial page of the chapter I want to download (usually page 1 or cover)
	2. Stream the source code
	3. Search for the image link
	4. Downloading the image link 
	5. Repat step until there is no image file detected (assumed that the last page of the chater reached)
	
Where to store the downloaded file?
	Default (Linux) = ~/.jmanga/manga/$MANGA_TITLE/$CHAPTER/

CLASS that might be needed (brainstorming stage):
	1. USR_DEFINED Class that store url and store method of manipulating the url get from the web
	2. USR_DEFINED Class called Manga
	3. Library to Scrap a web page and store it to a variable
	4. os library to later make compatibility for windows
	
NEXT RELEASE:
I WANT A MODULE, literaly another module and it should be easy to make new module like just stating the variabel without the method

NEXT NEXT RELEASE:
I WANT The module to be able to adapt if ANY website change its functionality