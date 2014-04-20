import wx
from wx.lib.scrolledpanel import ScrolledPanel
import sys


class ConfigPanel(ScrolledPanel):
    def __init__(self, parent, main):
        ScrolledPanel.__init__(self, parent)
        self.main = main
        self.control_to_key = {}
        self.immediate = True

        bbox = wx.BoxSizer(wx.HORIZONTAL)

        if not self.immediate:
            b_save = wx.Button(self, -1, "Save")
            b_reset = wx.Button(self, -1, "Reset")
            self.Bind(wx.EVT_BUTTON, self.OnSave, b_save)
            self.Bind(wx.EVT_BUTTON, self.OnReset, b_reset)
            bbox.Add(b_save, 1, wx.EXPAND)
            bbox.Add(b_reset, 1, wx.EXPAND)

        box = wx.BoxSizer(wx.VERTICAL)

        self.lc_grid = wx.FlexGridSizer(0, 2)
        self.lc_grid.AddGrowableCol(1)

        box.Add(self.lc_grid, 1, wx.EXPAND)
        box.Add(bbox, 0, wx.EXPAND)
        #box.Add(del_setup, 0, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()

        self.update()

    def update(self):
        self.lc_grid.Clear(True)
        self.control_to_key = {}
        config = self.main.client.get_config()

        for n, (key, value) in enumerate(config.items()):
            name = wx.StaticText(self, label=key)
            self.lc_grid.Add(name, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            if isinstance(value, bool):
                control = wx.CheckBox(self)
                evt = wx.EVT_CHECKBOX

            elif isinstance(value, int):
                control = wx.SpinCtrl(self, min=0, max=2**30)
                evt = wx.EVT_SPINCTRL

            elif isinstance(value, basestring):
                control = wx.TextCtrl(self)
                evt = wx.EVT_TEXT

            else:
                control = wx.TextCtrl(self)
                evt = wx.EVT_TEXT
                value = str(value)

            control.SetValue(value)
            self.Bind(evt, self.OnChange, control)
            self.control_to_key[control] = key
            self.lc_grid.Add(control, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)

        self.Layout()

    def OnChange(self, evt):
        if self.immediate:
            control = evt.GetEventObject()
            key = self.control_to_key[control]
            value = control.GetValue()
            self.main.client.set_config_value(key, value)

    def OnSave(self, evt):
        to_set = {}
        for control, key in self.control_to_key.items():
            to_set[key] = control.GetValue()
        self.main.client.set_config(to_set)

    def OnReset(self, evt):
        self.update()
