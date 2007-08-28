#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
#   
#   Copyleft 2006 limodou
#   
#   Distributed under the terms of the GPL (GNU Public License)
#   
#   UliPad is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id: mEditorCtrl.py 154 2005-11-07 04:48:15Z limodou $

import wx
import os
from modules import Mixin
from modules import common
from modules import makemenu

def add_tool_list(toollist, toolbaritems):
    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'new':(wx.ITEM_NORMAL, 'IDM_FILE_NEWS', 'images/new.gif', tr('new'), tr('Creates a new document'), 'OnFileNews'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list, Mixin.LOW)

def OnFileNews(win, event):
    if win.pref.syntax_select:
        eid = event.GetId()
        size = win.toolbar.GetToolSize()
        pos = win.toolbar.GetToolPos(eid)
        menu = wx.Menu()
        create_menu(win, menu)
        win.PopupMenu(menu, (size[0]*pos, size[1]))
        menu.Destroy()
    else:
        win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileNews', OnFileNews)

def pref_init(pref):
    pref.syntax_select = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 175, 'check', 'syntax_select', tr('Enable syntax selection as new file'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_FILE_NEWMORE',
        [
           (100, 'IDM_FILE_NEWMORE_NULL', tr('(empty)'), wx.ITEM_NORMAL, '', ''),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def init(win):
    if win.pref.syntax_select:
        menu = makemenu.findmenu(win.menuitems, 'IDM_FILE_NEWMORE')
        menu.Delete(win.IDM_FILE_NEWMORE_NULL)
        create_menu(win, menu)
Mixin.setPlugin('mainframe', 'init', init)

def create_menu(win, menu):
    ids = {}
    def _OnFileNew(event, win=win, ids=ids):
        lexname = ids.get(event.GetId(), '')
        if lexname:
            lexer = win.lexers.getNamedLexer(lexname)
            if lexer:
                templatefile = common.getConfigPathFile('template.%s' % lexer.name)
                if os.path.exists(templatefile):
                    text = file(templatefile).read()
                    text = common.decode_string(text)
                else:
                    text = ''
            document = win.editctrl.new(defaulttext=text, language=lexer.name)
    
    for name, lexname in win.filenewtypes:
        _id = wx.NewId()
        menu.Append(_id, "%s" % name)
        ids[_id] = lexname
        wx.EVT_MENU(win, _id, _OnFileNew)
    