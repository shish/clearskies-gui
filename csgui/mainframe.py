import logging

import wx
import wx.grid
import wx.html

from clearskies.client import ClearSkies
from clearskies.exc import ClientException
from csgui.common import icon_bundle, resource
from csgui.trayicon import TrayIcon

__version__ = "0.0.0"
log = logging.getLogger(__name__)


class MainFrame(wx.Frame):
    def __menu(self):
        menu_bar = wx.MenuBar()

        ################################################################
        menu = wx.Menu()
        m_create = menu.Append(wx.ID_ADD, "&Create Share\tAlt-C", "Create new share.")
        self.Bind(wx.EVT_MENU, self.OnCreate, m_create)
        m_attach = menu.Append(wx.ID_COPY, "&Attach Share\tAlt-A", "Attach to existing share.")
        self.Bind(wx.EVT_MENU, self.OnAttach, m_attach)
        menu.AppendSeparator()
        m_exit = menu.Append(wx.ID_EXIT, "")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menu_bar.Append(menu, "&File")

        ################################################################
        #menu = wx.Menu()
        #
        #menu_bar.Append(menu, "&Shares")

        ################################################################
        #menu = wx.Menu()
        #
        #m_start_tray = menu.Append(2021, "Start in Systray", "", kind=wx.ITEM_CHECK)
        #self.m_start_tray = m_start_tray  # event handler needs this object, not just ID?
        #if self.settings["start-tray"]:
        #    m_start_tray.Check(True)
        #self.Bind(wx.EVT_MENU, self.OnToggleStartTray, m_start_tray)
        #
        #menu_bar.Append(menu, "&Options")

        ################################################################
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menu_bar.Append(menu, "&Help")

        return menu_bar

    def __init_gui(self, parent):
        # init window
        try:
            # give this process an ID other than "python", else
            # windows 7 will give it the python icon and group it
            # with other python windows in the task bar
            import ctypes
            myappid = 'code.shishnet.org/csgui'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            pass

        wx.Frame.__init__(self, parent, -1, "CSGUI [%s]" % __version__, size=(640, 480))
        self.Bind(wx.EVT_CLOSE, self.OnWinClose)
        try:
            self.SetIcons(icon_bundle(resource("icon.ico")))
        except Exception as e:
            pass

        # bars
        self.SetMenuBar(self.__menu())
        self.statusbar = self.CreateStatusBar()

        # body of the window
        self.launcher = wx.Panel(self)
        self.tabs = wx.Notebook(self)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.launcher, 0, wx.EXPAND)
        box.Add(self.tabs, 1, wx.EXPAND)
        #self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

        # add content to tabs
        #self.news_panel = NewsPanel(self.tabs, "http://code.shishnet.org/eve-mlp/news.html")
        #self.config_panel = ConfigPanel(self.tabs, self)
        #self.status_panel = StatusPanel(self.tabs, self)
        #self.help_panel = NewsPanel(self.tabs, resource("help.html"))

        #self.tabs.AddPage(self.news_panel, "MLP News")
        #self.tabs.AddPage(self.config_panel, "Settings")
        #self.tabs.AddPage(self.status_panel, "Status")
        #self.tabs.AddPage(self.help_panel, "Help")

        # show the window and tray icon (if desired)
        show = True
        try:
            self.icon = TrayIcon(self)
            if self.settings["start-tray"]:
                log.info("Start-in-tray enabled, hiding main window")
                show = False
        except Exception as e:
            log.exception("Failed to create tray icon:")
            self.icon = None

        if show:
            self.Show(True)

    def __init__(self, parent):
        log.info("Loading settings")
        self.settings = {
            "start-tray": True,
        }

        self.client = ClearSkies()
        self.OnConnect(None)

        self.__init_gui(parent)

    def OnConnect(self, evt):
        try:
            log.info("Connecting to daemon")
            self.client.connect()
        except ClientException as e:
            dlg = wx.MessageDialog(
                None,
                "Error connecting to daemon:\n%s" % e,
                "CSGUI Error",
                wx.ICON_ERROR | wx.OK
            )
            dlg.ShowModal()
            log.exception("Error connecting to daemon: %s", e)

    def OnCreate(self, evt):
        log.info("Prompting to create")

        d_path = wx.DirDialog(
            self,
            "Choose which folder to share",
            # "default path",
        )
        if d_path.ShowModal() != wx.ID_OK:
            return
        path = d_path.GetPath()

        log.info("Creating new share %s", path)
        self.client.create_share(path)

    def OnAttach(self, evt):
        log.info("Prompting to attach")

        d_code = wx.TextEntryDialog(
            self,
            "Please enter the access code you have been\ngiven for this share (eg SYNC1234ABCD)",
            'Enter Access Code', ''
        )
        if d_code.ShowModal() != wx.ID_OK:
            return
        code = d_code.GetValue()

        d_path = wx.DirDialog(
            self,
            "Choose where to save this share",
            # "default path",
        )
        if d_path.ShowModal() != wx.ID_OK:
            return
        path = d_path.GetPath()

        log.info("Attaching %s to %s", code, path)
        self.client.add_share(code, path)

    def OnClose(self, evt):
        self.Close()

    def OnWinClose(self, evt):
        log.info("Saving config and exiting")
        if self.icon:
            self.icon.Destroy()
        self.Destroy()

    def OnToggleVisible(self, evt):
        if self.IsShown():
            self.Hide()
        else:
            self.Show()

    def OnToggleStartTray(self, evt):
        self.settings["start-tray"] = self.m_start_tray.IsChecked()

    def OnAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.SetName("CSGUI")
        info.SetDescription("A simple ClearSkies GUI")
        info.SetVersion(__version__)
        info.SetCopyright("(c) Shish 2014")
        info.SetWebSite("https://github.com/shish/csgui")
        info.AddDeveloper("Shish <webmaster@shishnet.org>")

        # Had some trouble with pyinstaller not putting these resources
        # in the places they should be, so make sure we can live without
        # them until the pyinstaller config gets fixed
        try:
            info.SetIcon(wx.Icon(resource("icon.ico"), wx.BITMAP_TYPE_ICO))
        except Exception as e:
            log.exception("Error getting icon:")

        try:
            info.SetLicense(file(resource("LICENSE.txt")).read())
        except Exception as e:
            log.exception("Error getting license:")
            info.SetLicense("GPL")

        wx.AboutBox(info)
