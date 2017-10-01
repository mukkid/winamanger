import win32gui

class Window():
	def __init__(self, hwnd, x, y, width, height):
		self.hwnd = hwnd
		self.x = x
		self.y = y
		self.width = width
		self.heigth = height

	def __len__(self):
		return (self.width, self.height)

	def __repr__(self):
		return f'Window({self.hwnd}, {self.x}, {self.y}, {self.width}, {self.height})'

class Screen():
	windows = {}

	def __init__(self):
		pass

	def _add_to_windows(self, hwnd, windows):
		if win32gui.GetWindowText(hwnd):
			self.windows[hwnd] = win32gui.GetWindowText(hwnd)

	def refresh(self):
		win32gui.EnumWindows(self._add_to_windows, self.windows)