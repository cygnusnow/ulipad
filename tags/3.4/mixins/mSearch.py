#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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
#   $Id: mSearch.py 1566 2006-10-09 04:44:08Z limodou $

"""Search process"""

import wx
from modules import Mixin
from modules import common

def add_mainframe_menu(menulist):
    menulist.extend([ (None, #parent menu id
        [
            (400, 'IDM_SEARCH', tr('Search'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_SEARCH', #parent menu id
        [
            (100, 'wx.ID_FIND', tr('Find...') + '\tE=Ctrl+F', wx.ITEM_NORMAL, 'OnSearchFind', tr('Find text')),
            (110, 'IDM_SEARCH_DIRECTFIND', tr('Direct Find') + '\tE=F4', wx.ITEM_NORMAL, 'OnSearchDirectFind', tr('Direct find selected text')),
            (120, 'wx.ID_REPLACE', tr('Replace...') + '\tE=Ctrl+H', wx.ITEM_NORMAL, 'OnSearchReplace', tr('Find and replace text')),
            (130, 'wx.ID_FORWARD', tr('Find Next') + '\tE=F3', wx.ITEM_NORMAL, 'OnSearchFindNext', tr('Find next occurance of text')),
            (140, 'wx.ID_BACKWARD', tr('Find Previous') + '\tE=Shift+F3', wx.ITEM_NORMAL, 'OnSearchFindPrev', tr('Find previous occurance of text')),
            (150, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (160, 'IDM_SEARCH_GOTO_LINE', tr('Go to Line...') + '\tE=Ctrl+G', wx.ITEM_NORMAL, 'OnSearchGotoLine', tr('Goes to specified line in the active document')),
            (170, 'IDM_SEARCH_LAST_MODIFY', tr('Go to Last Modify') + '\tE=Ctrl+B', wx.ITEM_NORMAL, 'OnSearchLastModify', tr('Goes to the last modify position')),

        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_mainframe_menu_image_list(imagelist):
    imagelist.update({
        'wx.ID_FIND':'images/find.gif',
        'wx.ID_REPLACE':'images/replace.gif',
        'wx.ID_FORWARD':'images/findnext.gif',
    })
Mixin.setPlugin('mainframe', 'add_menu_image_list', add_mainframe_menu_image_list)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (220, 'find'),
        (230, 'replace'),
        (240, '|'),
    ])

    toolbaritems.update({
        'find':(wx.ITEM_NORMAL, 'wx.ID_FIND', 'images/find.gif', tr('find'), tr('Find text'), 'OnSearchFind'),
        'replace':(wx.ITEM_NORMAL, 'wx.ID_REPLACE', 'images/replace.gif', tr('replace'), tr('Find and replace text'), 'OnSearchReplace'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def afterinit(win):
    import FindReplaceDialog

    win.finder = FindReplaceDialog.Finder()
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_set_focus(win, event):
    win.mainframe.finder.setWindow(win)
Mixin.setPlugin('editor', 'on_set_focus', on_set_focus)

def OnSearchFind(win, event):
    from modules import Resource
    from modules import i18n
    import FindReplaceDialog

    findresfile = common.uni_work_file('resources/finddialog.xrc')
    filename = i18n.makefilename(findresfile, win.app.i18n.lang)
    dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindDialog, 'FindDialog', win.finder)
    dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchFind', OnSearchFind)

def OnSearchDirectFind(win, event):
    text = win.document.GetSelectedText()
    if len(text) > 0:
        win.finder.findtext = text
        win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchDirectFind', OnSearchDirectFind)

def OnSearchReplace(win, event):
    from modules import Resource
    from modules import i18n
    import FindReplaceDialog

    findresfile = common.uni_work_file('resources/finddialog.xrc')
    filename = i18n.makefilename(findresfile, win.app.i18n.lang)
    dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindReplaceDialog, 'FindReplaceDialog', win.finder)
    dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchReplace', OnSearchReplace)

def OnSearchFindNext(win, event):
    win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchFindNext', OnSearchFindNext)

def OnSearchFindPrev(win, event):
    win.finder.find(1)
Mixin.setMixin('mainframe', 'OnSearchFindPrev', OnSearchFindPrev)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 120, 'num', 'max_number', tr('Max number of saved items:'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
    pref.max_number  = 20
    pref.findtexts = []
    pref.replacetexts = []
Mixin.setPlugin('preference', 'init', pref_init)

def OnSearchGotoLine(win, event):
    from modules import Entry
    document = win.document

    line = document.GetCurrentLine() + 1
    dlg = Entry.MyTextEntry(win, tr("Go to Line..."), tr("Enter the Line Number:"), str(line))
    answer = dlg.ShowModal()
    if answer == wx.ID_OK:
        try:
            line = int(dlg.GetValue())
        except:
            return
        else:
            document.GotoLine(line-1)
Mixin.setMixin('mainframe', 'OnSearchGotoLine', OnSearchGotoLine)

def editor_init(win):
    win.lastmodify = -1
Mixin.setPlugin('editor', 'init', editor_init, Mixin.HIGH)

def OnSearchLastModify(win, event):
    document = event.GetEventObject()
    if document.lastmodify > -1:
        document.GotoPos(document.lastmodify)
Mixin.setMixin('mainframe', 'OnSearchLastModify', OnSearchLastModify)

def OnModified(win, event):
    for flag in (wx.stc.STC_MOD_INSERTTEXT, wx.stc.STC_MOD_DELETETEXT,
        wx.stc.STC_PERFORMED_UNDO,
        wx.stc.STC_PERFORMED_REDO):
        if event.GetModificationType() & flag:
            win.lastmodify = event.GetPosition()
            return
Mixin.setPlugin('editor', 'on_modified', OnModified)
