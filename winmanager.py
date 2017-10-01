from collections import OrderedDict

import fuzzywuzzy
import win32gui
import win32con
import ctypes

class Window():
	def __init__(self, hwnd, x, y, width, height, name):
		self.hwnd = hwnd
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.name = name

	def __len__(self):
		return (self.width, self.height)

	def __repr__(self):
		return f'Window({self.hwnd}, {self.x}, {self.y}, {self.width}, {self.height}, {self.name})'

	def __eq__(self, other):
		return other.hwnd == self.hwnd

	def is_real(self):
	    if not win32gui.IsWindowVisible(self.hwnd):
	        return False
	    if win32gui.GetParent(self.hwnd) != 0:
	        return False
	    hasNoOwner = win32gui.GetWindow(self.hwnd, win32con.GW_OWNER) == 0
	    lExStyle = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
	    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
	      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
	        if win32gui.GetWindowText(self.hwnd):
	            return True
	    return False

	@staticmethod
	def is_real_from_hwnd(hwnd):
	    if not win32gui.IsWindowVisible(hwnd):
	        return False
	    if win32gui.GetParent(hwnd) != 0:
	        return False
	    hasNoOwner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
	    lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
	    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
	      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
	        if win32gui.GetWindowText(hwnd):
	            return True
	    return False


class Screen():
	windows = OrderedDict()

	def __init__(self):
		pass

	def _add_to_windows(self, hwnd, windows):
			left, top, right, bottom = win32gui.GetWindowRect(hwnd)
			width, height = right - left, bottom - top
			win = Window(hwnd, left, top, width, height, win32gui.GetWindowText(hwnd))
			if win.is_real():
				self.windows[hwnd] = win

	def get_windows(self):
	    '''Returns windows in z-order (top first)'''
	    user32 = ctypes.windll.user32
	    lst = []
	    top = user32.GetTopWindow(None)
	    if not top:
	        return lst
	    lst.append(top)
	    self._add_to_windows(top, self.windows)
	    while True:
	        next = user32.GetWindow(lst[-1], win32con.GW_HWNDNEXT)
	        if not next:
	            break
	        lst.append(next)
	        self._add_to_windows(next, self.windows)

	def refresh(self):
		self.get_windows()

	def bring_window_to_front(self, window):
		win32gui.ShowWindow(window.hwnd, 5)
		win32gui.SetForegroundWindow(window.hwnd)

	def find_window(self, name):
		names = [ window.name for window in self.windows.values() ]
		name, confidence = fuzzywuzzy.process.extractOne(name, names)
		for window in self.windows.values():
			if window.name == name:
				return window

	'''
	TODO: Freeze in layers
	freeze() and restore() not yet fully functional
	'''
	def freeze(self):
		self.frozen_windows = list(self.windows.values())

	def restore(self):
		for window in reversed(self.frozen_windows):
			if window.is_real():
				self.bring_window_to_front(window)
