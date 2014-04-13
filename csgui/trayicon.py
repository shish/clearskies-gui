import wx
import logging
import platform
import os

from clearskies.exc import ClientException
from csgui.common import resource, icon_bundle

log = logging.getLogger(__name__)


class TrayIcon(wx.TaskBarIcon):
    def __init__(self, main):
        wx.TaskBarIcon.__init__(self)
        self.main = main
        self.SetIcon(wx.Icon(resource("icon.ico"), wx.BITMAP_TYPE_ICO, desiredWidth=16, desiredHeight=16), "ClearSkies")
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.main.OnToggleVisible)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnPopup)

    def OnPopup(self, event):
        self.menu = wx.Menu()
        self._id_to_path = {}

        try:
            for n, share in enumerate(self.main.client.list_shares()):
                # TODO: make this into a submenu with open / detach / etc options
                log.info("Adding menu item for share: %s" % share)
                self._id_to_path[3000 + n] = share["path"]
                m_open = self.menu.Append(3000 + n, '%s\t%s' % (share["path"], share["status"]))
                self.Bind(wx.EVT_MENU, self.OnOpen, m_open)

            self.menu.AppendSeparator()
            m_create = self.menu.Append(wx.ID_ADD, '&Create New Share')
            self.Bind(wx.EVT_MENU, self.main.OnCreate, m_create)
            m_attach = self.menu.Append(wx.ID_OPEN, '&Attach To Share')
            self.Bind(wx.EVT_MENU, self.main.OnAttach, m_attach)
        except ClientException:
            m_connect = self.menu.Append(2000, 'C&onnect to Daemon')
            self.Bind(wx.EVT_MENU, self.main.OnConnect, m_connect)

        self.menu.AppendSeparator()
        m_about = self.menu.Append(wx.ID_ABOUT, 'A&bout')
        self.Bind(wx.EVT_MENU, self.main.OnAbout, m_about)
        m_exit = self.menu.Append(wx.ID_EXIT, 'E&xit')
        self.Bind(wx.EVT_MENU, self.main.OnClose, m_exit)
        self.PopupMenu(self.menu)

    def OnOpen(self, evt):
        path = self._id_to_path[evt.GetId()]
        log.info("Opening %s" % path)

        plat = platform.platform()
        if "Windows" in plat:
            os.startfile(path)
        elif "Darwin" in plat:
            os.system('open "%s"' % path)
        else:
            os.system('xdg-open "%s"' % path)
