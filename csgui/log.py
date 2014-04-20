import wx


class LogPanel(wx.Panel):
    def __init__(self, parent, main):
        wx.Panel.__init__(self, parent)
        self.main = main

        box = wx.BoxSizer(wx.VERTICAL)

        b_refresh = wx.Button(self, -1, "Refresh")
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, b_refresh)
        box.Add(b_refresh, 0, wx.EXPAND)

        self.log_area = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        box.Add(self.log_area, 1, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()

    def OnRefresh(self, evt):
        try:
            self.log_area.SetValue(self.main.client.get_log_data())
        except Exception:
            pass

