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
                log.info("Adding menu item for share: %s" % share)
                submenu = wx.Menu()

                self._id_to_path[submenu] = share["path"]

                m_open = submenu.Append(wx.ID_OPEN, 'Open')
                submenu.Bind(wx.EVT_MENU, self.OnOpen, m_open)

                m_create_code = submenu.Append(wx.ID_ADD, 'Create Access Code')
                submenu.Bind(wx.EVT_MENU, self.OnCreateCode, m_create_code)

                m_detach = submenu.Append(wx.ID_CLOSE, 'Detach')
                submenu.Bind(wx.EVT_MENU, self.OnDetach, m_detach)

                self.menu.AppendSubMenu(submenu, share["path"])

            self.menu.AppendSeparator()
            m_create = self.menu.Append(wx.ID_ADD, '&Create New Share')
            self.Bind(wx.EVT_MENU, self.main.OnCreate, m_create)
            m_attach = self.menu.Append(wx.ID_COPY, '&Attach To Share')
            self.Bind(wx.EVT_MENU, self.main.OnAttach, m_attach)
        except ClientException:
            m_connect = self.menu.Append(wx.ID_REFRESH, 'C&onnect to Daemon')
            self.Bind(wx.EVT_MENU, self.main.OnConnect, m_connect)

        self.menu.AppendSeparator()
        m_about = self.menu.Append(wx.ID_ABOUT, '')
        self.Bind(wx.EVT_MENU, self.main.OnAbout, m_about)
        m_exit = self.menu.Append(wx.ID_EXIT, '')
        self.Bind(wx.EVT_MENU, self.main.OnClose, m_exit)

        self.main.SetAcceleratorTable(wx.NullAcceleratorTable)
        self.PopupMenu(self.menu)

    def OnOpen(self, evt):
        path = self._id_to_path[evt.GetEventObject()]
        log.info("Opening %s" % path)

        plat = platform.platform()
        # FIXME: this is blocking...
        if "Windows" in plat:
            os.startfile(path)
        elif "Darwin" in plat:
            os.system('open "%s"' % path)
        else:
            os.system('xdg-open "%s"' % path)

    def OnCreateCode(self, evt):
        path = self._id_to_path[evt.GetEventObject()]
        log.info("Creating access code for %s" % path)

        mode = "read_write"

        code = self.main.client.create_access_code(path, mode)

        d_code = wx.TextEntryDialog(
            self.main,
            "Send this code to the other PC via a secure channel",
            'Access Code', code
        )
        d_code.ShowModal()


    def OnDetach(self, evt):
        path = self._id_to_path[evt.GetEventObject()]
        log.info("Detaching %s" % path)

        self.main.client.remove_share(path)
