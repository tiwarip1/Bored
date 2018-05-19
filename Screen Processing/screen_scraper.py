import win32ui

window_name = "Overwatch" # use EnumerateWindow for a complete list
wd = win32ui.FindWindow(None, window_name)
dc = wd.GetWindowDC() # Get window handle
j = dc.GetPixel (60,20)  # as practical and intuitive as using PIL!
print (j)
dc.DeleteDC() # necessary to handle garbage collection, otherwise code starts to slow down over many iterations