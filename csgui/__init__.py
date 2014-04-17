import sys
import logging
import argparse

log = logging.getLogger(__name__)


def main(args=sys.argv):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)19.19s %(levelname)4.4s %(message)s")
    logging.getLogger("csgui").setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='ClearSkies GUI')
    parser.add_argument('-d', '--daemon', help="path to the daemon, to start it on demand")
    parser.add_argument('-i', '--inspector', help="load WX Inspector for gui debugging", action="store_true", default=False)

    args = parser.parse_args(args[1:])

    # WX imports are ~really~ slow (sometimes 2-3 seconds when my laptop
    # is under load), so defer them until we're actually ready to start,
    # and after we've printed a log message to say "don't worry, the app
    # is alive, give it a minute to load"...
    if args.inspector:
        log.info("Loading Inspectable GUI")
        from wx.lib.mixins.inspection import InspectableApp
        import wx.lib.inspection
        app = InspectableApp(False)
        wx.lib.inspection.InspectionTool().Show()
    else:
        log.info("Loading Regular GUI")
        import wx
        app = wx.App()

    from csgui.mainframe import MainFrame
    frame = MainFrame(None, args.daemon)
    app.MainLoop()
