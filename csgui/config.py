import wx


class ConfigPanel(wx.Panel):
    def __init__(self, parent, main):
        wx.Panel.__init__(self, parent)
        self.main = main

        bbox = wx.BoxSizer(wx.HORIZONTAL)
        b_save = wx.Button(self, -1, "Save")
        b_reset = wx.Button(self, -1, "Reset")
        bbox.Add(b_save, 1, wx.EXPAND)
        bbox.Add(b_reset, 1, wx.EXPAND)

        box = wx.BoxSizer(wx.VERTICAL)

        self.lc_grid = wx.FlexGridSizer(0, 2)
        self.lc_grid.AddGrowableCol(1)

        #self.Bind(ulc.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.char_list)
        self.Bind(wx.EVT_BUTTON, self.OnSave, b_save)
        self.Bind(wx.EVT_BUTTON, self.OnReset, b_reset)

        box.Add(self.lc_grid, 1, wx.EXPAND)
        box.Add(bbox, 0, wx.EXPAND)
        #box.Add(del_setup, 0, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()

        self.update()

    def update(self):
        self.lc_grid.Clear(True)

        for n, (key, value) in enumerate(self.main.client.get_config().items()):
            name = wx.StaticText(self, label=key)
            self.lc_grid.Add(name, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            if isinstance(value, bool):
                check = wx.CheckBox(self, 4000 + n)
                check.SetValue(value)
                #self.Bind(wx.EVT_CHECKBOX, self.OnCheck, check)
                self.lc_grid.Add(check, 1, wx.ALIGN_CENTER_VERTICAL)

            elif isinstance(value, int):
                button = wx.TextCtrl(self, 4200 + n, str(value))
                #self.Bind(wx.EVT_BUTTON, self.OnLaunch, button)
                self.lc_grid.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            elif isinstance(value, basestring):
                button = wx.TextCtrl(self, 4200 + n, str(value))
                #self.Bind(wx.EVT_BUTTON, self.OnLaunch, button)
                self.lc_grid.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            else:
                button = wx.TextCtrl(self, 4200 + n, str(value))
                #self.Bind(wx.EVT_BUTTON, self.OnLaunch, button)
                self.lc_grid.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        self.Layout()

    def OnSave(self, evt):
        pass

    def OnReset(self, evt):
        pass