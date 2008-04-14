#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
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
#   $Id: mDirBrowser.py 1897 2007-02-03 10:33:43Z limodou $

import wx
import os
from modules import Mixin
from modules import Globals

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (115, 'dir'),
    ])

    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'dir':(wx.ITEM_CHECK, 'IDTM_DIRBROWSER', 'images/dir.gif', tr('Open Directory Browser'), tr('Opens directory browser window.'), 'OnToolbarDirBrowser'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def afterinit(win):
    wx.EVT_UPDATE_UI(win, win.IDTM_DIRBROWSER, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_mainframe_updateui(win, event):
    eid = event.GetId()
    if eid == win.IDTM_DIRBROWSER:
        page = win.panel.getPage(tr('Dir Browser'))
        event.Check(bool(page))
Mixin.setPlugin('mainframe', 'on_update_ui', on_mainframe_updateui)

def OnToolbarDirBrowser(win, event):
    page = win.panel.getPage(tr('Dir Browser'))
    if page:
        win.panel.closePage(tr('Dir Browser'))
    else:
        if win.createDirBrowserWindow():
            win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('mainframe', 'OnToolbarDirBrowser', OnToolbarDirBrowser)

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_FILE',
        [
            (138, 'IDM_WINDOW_DIRBROWSER', tr('Open Directory Browser')+'\tF2', wx.ITEM_NORMAL, 'OnWindowDirBrowser', tr('Opens directory browser window.'))
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([(None,
        [
            (170, 'IDPM_DIRBROWSERWINDOW', tr('Open Directory Browser'), wx.ITEM_NORMAL, 'OnDirBrowserWindow', tr('Opens directory browser window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_notebook_menu)

def afterinit(win):
    win.dirbrowser_imagelist = {
        'close':'images/folderclose.gif',
        'open':'images/folderopen.gif',
        'item':'images/file.gif',
    }
    if win.pref.open_last_dir_as_startup and win.pref.last_dir_paths:
        wx.CallAfter(win.createDirBrowserWindow, win.pref.last_dir_paths)
        wx.CallAfter(win.panel.showPage, tr('Dir Browser'))
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def createDirBrowserWindow(win, dirs=None):
    page = None
    if not win.panel.getPage(tr('Dir Browser')):
        from DirBrowser import DirBrowser

        if not dirs:
            dirs = win.pref.last_dir_paths
        page = DirBrowser(win.panel.createNotebook('left'), win, dirs)
        win.panel.addPage('left', page, tr('Dir Browser'))
    return page
Mixin.setMixin('mainframe', 'createDirBrowserWindow', createDirBrowserWindow)

def OnWindowDirBrowser(win, event):
    win.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('mainframe', 'OnWindowDirBrowser', OnWindowDirBrowser)

def OnDirBrowserWindow(win, event):
    win.mainframe.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('notebook', 'OnDirBrowserWindow', OnDirBrowserWindow)

def pref_init(pref):
    pref.recent_dir_paths = []
    pref.recent_dir_paths_num = 20
    pref.last_dir_paths = []
    pref.open_last_dir_as_startup = True
    pref.dirbrowser_last_addpath = os.getcwd()
    if wx.Platform == '__WXMSW__':
        cmdline = os.environ['ComSpec']
        pref.command_line = cmdline
    else:
        pref.command_line = 'gnome-terminal --working-directory={path}'
    pref.open_project_setting_dlg = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
#        (tr('General'), 100, 'num', 'recent_dir_paths_num', tr('Max number of recent browse directories:'), None),
        (tr('General'), 150, 'check', 'open_last_dir_as_startup', tr('Open last directory browser upon startup'), None),
        (tr('General'), 151, 'check', 'open_project_setting_dlg', tr('Auto open Project Setting Dialog when adding directory to Directory Browser Window'), None),
        (tr('General'), 160, 'openfile', 'command_line', tr('Command line of Open Command Window Here'), {'span':True}),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def after_addpath(dirbrowser, node):
    Globals.mainframe.pref.last_dir_paths = dirbrowser.getTopDirs()
    Globals.mainframe.pref.save()
Mixin.setPlugin('dirbrowser', 'after_addpath', after_addpath)

def after_closepath(dirbrowser, path):
    Globals.mainframe.pref.last_dir_paths = dirbrowser.getTopDirs()
    Globals.mainframe.pref.save()
Mixin.setPlugin('dirbrowser', 'after_closepath', after_closepath)

def afterclosewindow(win):
    win.panel.showWindow('LEFT', False)
    win.panel.showWindow('bottom', False)
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)