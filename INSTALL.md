
Setup
-----
```
$ sudo apt-get install python-wxgtk2.8    # debian / ubuntu
$ sudo yum install wxPython               # red hat / fedora / centos

$ sudo pip install -e ./                  # install clearskies / csgui commands
$ ./launch.py                             # or run straight from the source folder
```

Building Binaries
-----------------
Requires `python` and `git` commands in the path, and pyinstaller in
../pyinstaller-2.0/, as well as the python module dependencies from
the app itself.

Though TBH, if you can be bothered to set up a large dev environment
with extras for .exe building, you might as well just set up a small
dev environment and run from source...

