#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import ttk 
import tkMessageBox
import os
import sys
import threading
from Module import youkuClass
from Module import tudouClass
from Module import sohuClass
from Module import letvClass

class GUI :

	def __init__ (self) :
		self.masterTitle = 'Video Downloader'
		self.slaveTitle = 'Info'

	def __mainWindow (self) :
		self.master = Tkinter.Tk();

		self.master.title(self.masterTitle)
		self.master.resizable(width = 'false', height = 'false')

		self.__menu()
		self.__topBox()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		filemenu = Tkinter.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "Info", command = self.__showInfo)
		filemenu.add_command(label = "Quit", command = self.master.quit)
		menubar.add_cascade(label = "About", menu = filemenu)

		self.master.config(menu = menubar)

	def __topBox (self) :
		self.mainTop = Tkinter.Frame(self.master, bd = 10)
		self.mainTop.grid(row = 0, column = 0, sticky = '')		

		self.urlInput = Tkinter.Entry(self.mainTop, width = 50)
		self.urlInput.grid(row = 0, column = 0)

		s = self.__selector(self.mainTop)
		s.grid(row = 0, column = 1)

		self.__searchBtn()


	def __selector (self, position) :
		self.selectorVal = Tkinter.StringVar()
		self.selectorVal.set("HD")

		videoType = ['HD', '超清', '高清']

		s = ttk.Combobox(position, width = 5, textvariable = self.selectorVal, state='readonly', values = videoType)

		return s	

	def __showResult (self) :
		self.mainFoot = Tkinter.Frame(self.master, bd = 10)
		self.mainFoot.grid(row = 1, column = 0, sticky = '')		

		self.__searchBtn(False)

		threading.Thread(target = self.__getUrl).start()

		# b = Tkinter.Button(mainFoot, text = '下载', command = '')
		# b.grid(row = 1, column = 0, sticky = 'ew')

	def __getUrl (self):
		url = self.urlInput.get()
		result = True
		if 'youku' in url :
			getClass = youkuClass.ChaseYouku()
		elif 'sohu' in url :
			getClass = sohuClass.ChaseSohu()
		elif 'letv' in url :
			getClass = letvClass.ChaseLetv()
		elif 'tudou' in url :
			getClass = tudouClass.ChaseTudou()
		else :
			result = False

		if result :
			result = ''
			videoType = self.selectorVal.get()

			if videoType == u'HD' :
				videoType = 's'
			elif videoType == u'超清' :
				videoType = 'h'
			elif videoType == u'高清' :
				videoType = 'n'
			else :
				videoType = 's'

			getClass.videoLink = url
			getClass.videoType = videoType
			urlList = getClass.chaseUrl()

			if urlList['stat'] == 0 :
				i = 1
				for x in urlList['msg']:
					result += '第' + str(i) + '段:\n' + str(x) + '\n'
					i += 1
			else :
				result = urlList['msg']

		else :
			result = '链接地址不再分析范围内！'

		
		self.resultWindow = Tkinter.Text(self.mainFoot, height = 5, width = 70, highlightthickness = 0)
		self.resultWindow.grid(row = 0, sticky = '')
		self.resultWindow.insert('end', result)

		self.__searchBtn()


	def __searchBtn (self, stat = True) :
		if stat :
			b = Tkinter.Button(self.mainTop, text = '搜索', command = self.__showResult)
			b.grid(row = 0, column = 2)
		else :
			b = Tkinter.Button(self.mainTop, text = '稍等', command = '')
			b.grid(row = 0, column = 2)


	def __showInfo(self):
		self.slave = Tkinter.Tk();

		self.slave.title(self.slaveTitle)
		self.slave.resizable(width = 'false', height = 'false')

		info = [
			'Virsion: Beta 0.9.0',
			'Support: www.youku.com\rwww.tudou.com\rtv.sohu.com\rwww.letv.com',
			'Website: https://github.com/EvilCult/Video-Downloader',
			'Author: Ray H.'
		]

		label = Tkinter.Label(self.slave, text="Video Downloader", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		label.grid(row = 0)
		i = 1
		for n in info :
			label = Tkinter.Label(self.slave, text = n.split(': ')[0], font = ("Helvetica", "14", 'bold'), anchor = 'center')
			label.grid(row = i)
			label = Tkinter.Label(self.slave, text = n.split(': ')[1], font = ("Helvetica", "12"), anchor = 'center')
			label.grid(row = (i + 1))
			i += 2

	def run (self) :
		self.__mainWindow()
		self.master.mainloop()