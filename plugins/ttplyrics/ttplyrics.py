# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*- 
#
# Copyright 2007 Sevenever
# Copyright (C) 2007 Sevenever
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import os
import gtk, gobject
import urllib
import re
from xml.dom import minidom
import rb
import rhythmdb
from ttpClient import ttpClient
import random
import locale

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ViewMenu" action="View">
      <menuitem name="ttplyrics" action="TTPLyrics"/>
    </menu>
  </menubar>
</ui>
"""

LYRICS_FOLDER="~/.lyrics"
LYRIC_TITLE_STRIP=["\(live[^\)]*\)", "\(acoustic[^\)]*\)", "\([^\)]*mix\)", "\([^\)]*version\)", "\([^\)]*edit\)", "\(feat[^\)]*\)"]
LYRIC_TITLE_REPLACE=[("/", "-"), (" & ", " and ")]
LYRIC_ARTIST_REPLACE=[("/", "-"), (" & ", " and ")]

MAX_RETRY = 5

def create_lyrics_view():
    view = gtk.TextView()
    view.set_wrap_mode(gtk.WRAP_WORD)
    view.set_editable(False)

    sw = gtk.ScrolledWindow()
    sw.add(view)
    sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    sw.set_shadow_type(gtk.SHADOW_IN)

    vbox = gtk.VBox(spacing=12)
    vbox.pack_start(sw, expand=True)
    return (vbox, view.get_buffer())

class TTPLyricWindow(gtk.Window):
    def __init__(self, parent):
        gtk.Window.__init__(self)
	
	self.lyrics_grabber = TTPLyricGrabber()
	
        self.set_border_width(12)
	self.set_transient_for(parent)

	self.set_title(_('ttplyrics by sevenever'))

	close = gtk.Button(stock=gtk.STOCK_CLOSE)
	close.connect('clicked', lambda w: self.destroy())

	(lyrics_view, buffer) = create_lyrics_view()
	self.buffer = buffer
        bbox = gtk.HButtonBox()
        bbox.set_layout(gtk.BUTTONBOX_END)
        bbox.pack_start(close)
        lyrics_view.pack_start(bbox, expand=False)
	
        self.add(lyrics_view)
        self.set_default_size(400, 600)
        self.show_all()

    def show_lyrics(self, entry, shell):
	db = shell.props.db
	title = db.entry_get(entry, rhythmdb.PROP_TITLE)
	artist = db.entry_get(entry, rhythmdb.PROP_ARTIST)
        self.set_title(title + " - " + artist + " - Lyrics")
	
        self.buffer.set_text(_("Searching for lyrics..."))
	self.lyrics_grabber.get_lyrics(db, entry, self.buffer.set_text)

class TTPLyricGrabber(object):
    def __init__(self):
    	self.loader = rb.Loader ()

    def _build_cache_path(self, artist, title):
        lyrics_folder = os.path.expanduser (LYRICS_FOLDER)
        if not os.path.exists (lyrics_folder):
            os.mkdir (lyrics_folder)

	artist_folder = lyrics_folder + '/' + artist[:128].encode(locale.getdefaultlocale()[1])
	if not os.path.exists (artist_folder):
	    os.mkdir (artist_folder)

	return artist_folder + '/' + title[:128].encode(locale.getdefaultlocale()[1]) + '.lyric'

    def get_lyrics(self, db, entry, callback):
	self.callback = callback
        artist = db.entry_get(entry, rhythmdb.PROP_ARTIST).lower()
        title = db.entry_get(entry, rhythmdb.PROP_TITLE).lower()

	# replace ampersands and the like
	for exp in LYRIC_ARTIST_REPLACE:
		p = re.compile (exp[0])
		artist = p.sub(exp[1], artist)
	for exp in LYRIC_TITLE_REPLACE:
		p = re.compile (exp[0])
		title = p.sub(exp[1], title)

        # strip things like "(live at Somewhere)", "(accoustic)", etc
        for exp in LYRIC_TITLE_STRIP:
            p = re.compile (exp)
            title = p.sub ('', title)

	# compress spaces
	title = title.strip()
	artist = artist.strip()

	self.cache_path = self._build_cache_path(artist, title)

	if os.path.exists (self.cache_path):
            self.loader.get_url(self.cache_path, callback)
            return;

	callback('Get Lyrics list on TTplayer lyrics server...')
	self.theurl = 'http://lrcct2.ttplayer.com/dll/lyricsvr.dll?sh?Artist=%s&Title=%s&Flags=0' % (ttpClient.EncodeArtTit(artist.replace(' ','').lower()), ttpClient.EncodeArtTit(title.replace(' ','').lower()))
	self.retry = 1
	self.loader.get_url(self.theurl, self.search_results)
	

    def search_results(self, data):
    	if data is None:
	    if self.retry < MAX_RETRY:
		self.retry += 1
		self.callback(str(self.retry) + 'th retry...')
		self.loader.get_url(self.theurl, self.search_results)		
		return
	    else:
		self.callback("Server did not respond.")
		return

	try:
	    dom1=minidom.parseString(data)
	    resultli = dom1.getElementsByTagName('lrc')
	    li = []
	    for node in resultli:
		li.append((node.getAttribute('id'),node.getAttribute('artist'),node.getAttribute('title')))
	except:
	    self.callback("Couldn't parse search results.")
	    return
	
	if len(li)==0:
	    self.callback('No lyrics found')
	    return
	Id,artist,title = li[0]
	
	self.theurl = 'http://lrcct2.ttplayer.com/dll/lyricsvr.dll?dl?Id=%d&Code=%d&uid=01&mac=%012x' % (int(Id),ttpClient.CodeFunc(int(Id), (artist + title).encode('UTF8')), random.randint(0,0xFFFFFFFFFFFF))
	
	self.loader.get_url(self.theurl, self.lyrics)


    def lyrics(self, data):
        if data is None:
	    if self.retry < MAX_RETRY:
		self.retry += 1
		self.callback((self.retry) + 'th retry...')
		self.loader.get_url(self.theurl, self.lyrics)		
		return
	    else:
		self.callback("Error occored while fetch lyrics content")
		return
	
	text = data
	text += "\n\n"+_("Lyrics provided by www.ttplayer.com")
	text += "\n\n"+_("ttplyrics plugin by sevenever")

        f = file (self.cache_path, 'w')
        f.write (text)
        f.close ()

	self.callback(text)


class TTPLyricsDisplayPlugin(rb.Plugin):

    def __init__ (self):
	rb.Plugin.__init__ (self)
	self.window = None

    def activate (self, shell):
	self.action = gtk.Action ('TTPLyrics', _('_TTPLyrics'),
				  _('View lyrics from ttplayer <http://www.ttplayer.com>'),
				  'rb-song-lyrics')
	self.activate_id = self.action.connect ('activate', self.show_lyrics_window, shell)

	self.action_group = gtk.ActionGroup ('TTPLyricsPluginActions')
	self.action_group.add_action (self.action)

    	uim = shell.get_ui_manager ()
	uim.insert_action_group (self.action_group, 0)
	self.ui_id = uim.add_ui_from_string (ui_str)
	uim.ensure_update ()

	sp = shell.get_player ()
	self.pec_id = sp.connect('playing-song-changed', self.playing_entry_changed, shell)
	self.playing_entry_changed (sp, sp.get_playing_entry (), shell)

    def deactivate (self, shell):

	uim = shell.get_ui_manager()
	uim.remove_ui (self.ui_id)
	uim.remove_action_group (self.action_group)

	self.action_group = None
	self.action = None

	sp = shell.get_player ()
	sp.disconnect (self.pec_id)
	
	if self.window is not None:
	    self.window.destroy ()
	
    def playing_entry_changed (self, sp, entry, shell):
    	if entry is not None:
	    self.show_song_lyrics(None, shell)

    def show_lyrics_window(self, action, shell):
	self.window = TTPLyricWindow(shell.props.window)
	self.window.show_all()
	sp = shell.get_player ()
	entry = sp.get_playing_entry ()
	self.playing_entry_changed(sp, entry, shell)
    
    def show_song_lyrics (self, action, shell):
	sp = shell.get_player ()
	entry = sp.get_playing_entry ()

	if entry is None:
	    return
	
	if self.window is None:
	    return

	self.window.show_lyrics(entry, shell)
