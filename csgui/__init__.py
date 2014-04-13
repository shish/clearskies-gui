import sys
import logging

from wx.lib.mixins.inspection import InspectableApp

from csgui.mainframe import MainFrame


def main(args=sys.argv):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)19.19s %(levelname)4.4s %(message)s")
    module_log = logging.getLogger("csgui")
    module_log.setLevel(logging.DEBUG)

    app = InspectableApp(False)
    frame = MainFrame(None)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
