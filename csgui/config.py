import wx


class ConfigPanel(wx.Panel):
    def __init__(self, parent, main):
        wx.Panel.__init__(self, parent)
        self.main = main

        box = wx.BoxSizer(wx.VERTICAL)

        #box.Add(foo, 1, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()
