import win32gui
import win32con

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


class Screen():
	windows = {}

	def __init__(self):
		pass

	def _add_to_windows(self, hwnd, windows):
			left, top, right, bottom = win32gui.GetWindowRect(hwnd)
			width, height = right - left, bottom - top
			win = Window(hwnd, left, top, width, height, win32gui.GetWindowText(hwnd))
			if win.is_real():
				self.windows[hwnd] = win

	def refresh(self):
		win32gui.EnumWindows(self._add_to_windows, self.windows)

	def bring_window_to_front(self, window):
		win32gui.ShowWindow(window.hwnd, 5)
		win32gui.SetForegroundWindow(window.hwnd)
