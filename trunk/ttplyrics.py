#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys
import locale
import codecs
import urllib2
import random
from xml.dom.minidom import parse, parseString

def CodeFunc(Id, data):
	length = len(data)
	
	tmp2=0
	tmp3=0
	
	tmp1 = (Id & 0x0000FF00) >> 8							#右移8位后为0x0000015F
															#tmp1 0x0000005F
	if ( (Id & 0x00FF0000) == 0 ):
		tmp3 = 0x000000FF & ~tmp1							#CL 0x000000E7
	else:
		tmp3 = 0x000000FF & ((Id & 0x00FF0000) >> 16)		#右移16位后为0x00000001
	
	tmp3 = tmp3 | ((0x000000FF & Id) << 8)					#tmp3 0x00001801
	tmp3 = tmp3 << 8										#tmp3 0x00180100
	tmp3 = tmp3 | (0x000000FF & tmp1)						#tmp3 0x0018015F
	tmp3 = tmp3 << 8										#tmp3 0x18015F00
	if ( (Id & 0xFF000000) == 0 ) :
		tmp3 = tmp3 | (0x000000FF & (~Id))					#tmp3 0x18015FE7
	else :
		tmp3 = tmp3 | (0x000000FF & (Id >> 24))			#右移24位后为0x00000000
	
	#tmp3	18015FE7
	
	i=length-1
	while(i >= 0):
		char = ord(data[i])
		if char >= 0x80:
			char = char - 0x100
		tmp1 = (char + tmp2) & 0x00000000FFFFFFFF
		tmp2 = (tmp2 << (i%2 + 4)) & 0x00000000FFFFFFFF
		tmp2 = (tmp1 + tmp2) & 0x00000000FFFFFFFF
		#tmp2 = (ord(data[i])) + tmp2 + ((tmp2 << (i%2 + 4)) & 0x00000000FFFFFFFF)
		i -= 1
	
	#tmp2 88203cc2
	i=0
	tmp1=0
	while(i<=length-1):
		char = ord(data[i])
		if char >= 128:
			char = char - 256
		tmp7 = (char + tmp1) & 0x00000000FFFFFFFF
		tmp1 = (tmp1 << (i%2 + 3)) & 0x00000000FFFFFFFF
		tmp1 = (tmp1 + tmp7) & 0x00000000FFFFFFFF
		#tmp1 = (ord(data[i])) + tmp1 + ((tmp1 << (i%2 + 3)) & 0x00000000FFFFFFFF)
		i += 1
	
	#EBX 5CC0B3BA
	
	#EDX = EBX | Id
	#EBX = EBX | tmp3
	tmp1 = (((((tmp2 ^ tmp3) & 0x00000000FFFFFFFF) + (tmp1 | Id)) & 0x00000000FFFFFFFF) * (tmp1 | tmp3)) & 0x00000000FFFFFFFF
	tmp1 = (tmp1 * (tmp2 ^ Id)) & 0x00000000FFFFFFFF
	
	if tmp1 > 0x80000000:
		tmp1 = tmp1 - 0x100000000
	return tmp1

def EncodeArtTit(str):
	rtn = ''
	str = str.encode('UTF-16')[2:]
	for i in range(len(str)):
		rtn += '%02x' % ord(str[i])
	
	return rtn

def GetLyricsList(artist, title):
	try:
		theurl = 'http://lrcct2.ttplayer.com/dll/lyricsvr.dll?sh?Artist=%s&Title=%s&Flags=0' % (EncodeArtTit(artist.replace(' ','').lower()), EncodeArtTit(title.replace(' ','').lower()))
		print theurl
		txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
		req = urllib2.Request(theurl, None, txheaders)
		# create a request object
		
		handle = urllib2.urlopen(req)
		# and open it to return a handle on the url
	except IOError, e:
		print 'We failed to open "%s".' % theurl
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code
		elif hasattr(e, 'reason'):
			print "The error object has the following 'reason' attribute :"
			print e.reason
		return False
	else:
		dom1=parseString(handle.read())
		list = dom1.getElementsByTagName('lrc')
		li = []
		for node in list:
			li.append((node.getAttribute('id'),node.getAttribute('artist'),node.getAttribute('title')))
		return li
def GetLyricsContent(Id,artist,title):
	try:
		theurl = 'http://lrcct2.ttplayer.com/dll/lyricsvr.dll?dl?Id=%d&Code=%d&uid=01&mac=%012x' % (int(Id),CodeFunc(int(Id), (artist + title).encode('UTF8')), random.randint(0,0xFFFFFFFFFFFF))
		print theurl
		txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
		req = urllib2.Request(theurl, None, txheaders)
		# create a request object
		
		handle = urllib2.urlopen(req)
		# and open it to return a handle on the url
	except IOError, e:
		print 'We failed to open "%s".' % theurl
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code
		elif hasattr(e, 'reason'):
			print "The error object has the following 'reason' attribute :"
			print e.reason
		return False
	else:
		return handle.read().decode('UTF8')
	

def main():
	artist = sys.argv[1].decode(locale.getdefaultlocale()[1])
	title = sys.argv[2].decode(locale.getdefaultlocale()[1])
	print 'Searching ', artist, title, '...'
	
	li = GetLyricsList(artist,title)
	
	if len(li) > 0:
		j=0
		for i in li:
			print j+1,': ', i[1], i[2]
			j+=1
			
		try:
			command=raw_input('Choise:')
		except EOFError:
			command=='0'
		
		command = int(command) - 1
		if command>=0 and command<len(li):
			print GetLyricsContent(li[command][0],li[command][1],li[command][2])
	else:
		print 'No lyrics found'

	return 0


if __name__ == '__main__':
	main()

