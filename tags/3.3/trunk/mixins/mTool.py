#       Programmer:     limodou
#       E-mail:         limodou@gmail.com
#
#       Copyleft 2006 limodou
#
#       Distributed under the terms of the GPL (GNU Public License)
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
#       $Id: mTool.py 1457 2006-08-23 02:12:12Z limodou $

import wx
from modules import Mixin

__doc__ = 'Tool menu'

def add_menu(menulist):
    menulist.extend([(None,
        [
            (550, 'IDM_TOOL', tr('Tool'), wx.ITEM_NORMAL, None, ''),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_menu)
