import wx
import main
import threading


class Frames(wx.Frame):
	def __init__(self, parent,id, title):    
		super(Frames, self).__init__(parent, title=title,  \
            size=(550, 350))
		self.InitUI()
		self.Centre()
		self.Show(True)  
	def InitUI(self):
		panel = wx.Panel(self)
		faicon = wx.Icon('norin.ico', wx.BITMAP_TYPE_ICO,32,32)
		self.SetIcon(faicon)
		self.mangaNameLabel = wx.StaticText(panel, label="Manga Name")
		self.mangaNameCtrl = wx.TextCtrl(panel, value="enter manga name here...")
		self.firstChapterLabel= wx.StaticText(panel, label="first chapter you want to download")
		self.firstChapterCtrl = wx.TextCtrl(panel, value="enter the first chapter you want to download here")
		self.endChapterLabel = wx.StaticText(panel, label="Last chapter you want to download")
		self.endChapterCtrl = wx.TextCtrl(panel, value="enter the last chapter you want to download here")
		self.loggerLabel= wx.StaticText(panel, label="logger")
		self.loggerCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.downloadButton = wx.Button(panel, label="Download !")
		self.icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('logo.png'))
		sizer = wx.GridBagSizer(6, 5)
		sizer.Add(self.mangaNameLabel, pos=(0,0), flag=wx.TOP  , border = 15)
		sizer.Add(self.mangaNameCtrl, pos=(0,1), span=(1,4) , flag= wx.EXPAND | wx.TOP  , border = 10 )
		sizer.Add(self.firstChapterLabel, pos=(1,0), flag=wx.TOP |wx.LEFT, border = 5 )
		sizer.Add(self.firstChapterCtrl, pos=(1,1), span=(1,4), flag = wx.TOP | wx.RIGHT | wx.EXPAND, border = 5)
		sizer.Add(self.endChapterLabel, pos=(2,0), flag = wx.LEFT | wx.TOP , border = 5)
		sizer.Add(self.endChapterCtrl, pos=(2,1), span=(1,4) ,flag= wx.TOP | wx.RIGHT| wx.EXPAND, border = 5)
		sizer.Add(self.loggerLabel, pos=(4,0), flag= wx.TOP | wx.LEFT | wx.EXPAND, border = 15)
		sizer.Add(self.loggerCtrl, pos=(4,1), span=(1,4),flag=  wx.TOP | wx.EXPAND | wx.BOTTOM ,border=5)
		sizer.Add(self.downloadButton, pos=(5,5), flag = wx.EXPAND | wx.RIGHT, border=5)
		sizer.Add(self.icon, pos=(5,0), span=(2,3), flag = wx.LEFT|wx.TOP | wx.ALIGN_LEFT , border=5)
		sizer.AddGrowableCol(1)
		sizer.AddGrowableRow(5)
		panel.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON,self.onSubmit)
		self.Bind(main.EVT_LOGGER, self.onLog)	
		
	def onLog(self, event):
		self.loggerCtrl.AppendText(event.data1)
	def onSubmit(self, event):
		
		manga_name = self.mangaNameCtrl.GetValue()
		first_chapter = self.firstChapterCtrl.GetValue()
		end_chapter = self.endChapterCtrl.GetValue()
		jmanga = main.Mangacanblog(manga_name)
		t = threading.Thread(target=jmanga.get_all_image , args=(first_chapter,end_chapter,self, ))
		t.setDaemon(True)
		t.start()
		#jmanga = Mangacanblog() DOIT LATER AFTER THE INTERFACE FINISH

		
		
		
app=wx.App()
Frames(None, -1 , 'Norin - No or Internet Manga Assistant')
app.MainLoop()
		
""""		LATER
manga_name = raw_input('masukan nama seri : ')
manga_chap = raw_input('masukan chapter :')
manga_chapend = raw_input('mau download sampe chater berapa? :')
jmanga= Mangacanblog(manga_name)
print "get manga link...."
print jmanga.get_all_image(manga_chap,manga_chapend)
"""