import pyautogui
from PIL import Image
import time
import math
import os
import pyautogui
from typing import *
import time
from numba import jit

from pynput import keyboard
import time
from threading import Thread

# Keyboard Listener for Control (Exit/Force Exit) and Shift (Speed)
break_program = False


def on_press(key):
	global break_program
	if key == keyboard.Key.ctrl:  # ctrl to exit
		break_program = True
		exit()
	if key == keyboard.Key.shift:  # shift to make it faster
		pyautogui.PAUSE = 0


def keyboardListener():
	with keyboard.Listener(on_press=on_press) as listener:
		while break_program == False:
			time.sleep(1)
		listener.join()


Thread(target=keyboardListener).start()

# Time Constants
pyautogui.PAUSE = 0.0015  # default 0.001
pyautogui.FAILSAFE = False
pyautogui.DARWIN_CATCH_UP_TIME = 0.0035

# JS Paint
JSPaintColors: dict = {
	(0, 1, 0): (40, 845),
	(255, 255, 255): (41, 859),
	(128, 128, 128): (58, 846),
	(193, 192, 191): (58, 859),
	(234, 52, 35): (72, 861),
	(117, 20, 12): (74, 844),
	(128, 128, 38): (89, 845),
	(255, 255, 84): (90, 858),
	(55, 126, 33): (106, 847),
	(117, 251, 76): (105, 861),
	(55, 126, 127): (120, 846),
	(117, 251, 253): (121, 857),
	(0, 0, 123): (136, 847),
	(0, 0, 245): (137, 861),
	(117, 20, 124): (153, 846),
	(234, 51, 247): (153, 861),
	(128, 128, 72): (169, 847),
	(255, 254, 146): (171, 860),
	(24, 63, 63): (187, 845),
	(118, 251, 141): (186, 859),
	(55, 126, 247): (202, 845),
	(161, 252, 253): (201, 861),
	(24, 63, 124): (217, 846),
	(128, 127, 248): (217, 860),
	(57, 5, 245): (232, 847),
	(233, 51, 127): (234, 861),
	(119, 67, 20): (249, 847),
	(239, 134, 79): (250, 860)
}

# Gartic Phone
GarticColors: dict = {(0, 0, 0): (352, 449), (102, 102, 102): (399, 452), (0, 80, 205): (451, 451), (255, 255, 255): (354, 495), (170, 170, 170): (403, 496), (38, 201, 255): (449, 499), (1, 116, 32): (356, 549), (153, 0, 0): (405, 548), (150, 65, 18): (
	444, 549), (17, 176, 60): (357, 598), (255, 0, 19): (406, 593), (255, 120, 41): (446, 593), (176, 112, 28): (352, 642), (153, 0, 78): (396, 644), (203, 90, 87): (454, 644), (255, 193, 38): (357, 689), (255, 0, 143): (400, 688), (254, 175, 168): (444, 694)}

# Scribbl.io
ScribblioColors: dict = {
	(255, 255, 255): (339, 853),
	(0, 0, 0): (337, 879),
	(193, 193, 193): (361, 853),
	(76, 76, 76): (361, 884),
	(219, 52, 37): (386, 854),
	(106, 24, 16): (385, 879),
	(238, 121, 48): (414, 855),
	(179, 67, 29): (412, 880),
	(251, 229, 77): (433, 856),
	(222, 165, 56): (432, 881),
	(92, 201, 59): (460, 853),
	(34, 84, 28): (455, 878),
	(79, 175, 249): (479, 853),
	(35, 85, 153): (483, 879),
	(34, 31, 203): (505, 858),
	(13, 8, 97): (507, 882),
	(149, 29, 180): (529, 856),
	(77, 10, 101): (529, 881),
	(199, 128, 168): (555, 856),
	(156, 89, 115): (555, 880),
	(150, 86, 53): (576, 855),
	(92, 51, 22): (577, 879)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class DrawBot:
	def __init__(self) -> None:
		super().__init__()

		self.ColorWithCoords: dict = {}
		self.Colors: dict = GarticColors
		self.ColorMap = {}

		self.White: tuple = (255, 255, 255)

		self.SameColor: int = 1

		self.u_agnt: dict = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.473',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive', }

		self.Image_Folder: str = 'Img'

	def Change_Color(self, xyT: tuple):
		# xyT is a tuple of x and y coordinates like (100, 200)
		pyautogui.moveTo(xyT)
		time.sleep(0.5)
		pyautogui.click(clicks=2)

	def click(self, New_X: int, New_Y: int):
		pyautogui.click(New_X, New_Y)

	def drag(self, X1: int, X2: int, Y: int):
		pyautogui.moveTo(X1, Y)
		pyautogui.dragTo(X2, Y, button='left')

	@staticmethod
	@jit(nopython=True)
	def closest_color_helper(r, cr, g, cg, b, cb):
		return math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)

	def closest_color(self, rgb: tuple) -> tuple:
		"""
		Find the closest color in the color dictionary
		using the Euclidean distance algorithm.
		and then return the closest color
		"""
		if rgb in self.ColorMap:
			return self.ColorMap[rgb]
		else:
			r, g, b = rgb[:3]
			maxdiff = 999
			for color in self.Colors:
				cr, cg, cb = color
				color_diff = self.closest_color_helper(r, cr, g, cg, b, cb)
				if color_diff < maxdiff:
					closestColor = color
					maxdiff = color_diff
			self.ColorMap[rgb] = closestColor
			return closestColor

	def match_color(self, rgb: tuple) -> tuple:
		return self.Colors.get(rgb)

	def resizeImage(self, imageName: str) -> Image.Image:
		"""
						Resizes the image to a smaller size. For fitting on canvas
						Not Mandatory
		"""
		image = Image.open(imageName)
		width, height = image.size
		image = image.resize(
			(min(700, round(400*width/height)), 400), Image.LANCZOS)
		# image = image.resize((400, 400), Image.ANTIALIAS)
		return image

	@staticmethod
	def getConsecutivePixels(nums: Iterator) -> list:
		"""
						Uses Magic to find the consecutive pixels, and
						returns an array of the pixel ranges.

						Ex:
										(x, y), (1, 2, 3, 4, 5, 7, 8, 9, 10)
										will become
										(1, 5), (7, 10) indicating x values from 1 to 5, and 7 to 10.
		"""
		gaps: list = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
		edges: iter = iter(nums[:1] + sum(gaps, []) + nums[-1:])
		return [i for i in zip(edges, edges) if abs(i[0] - i[1]) > 3]

	def optimize(self, colorwithcoords: Tuple[Tuple[Tuple[int], Tuple[int]]]) -> Tuple[Tuple[Tuple], Dict[int, Tuple[int]]]:
		"""
		detect consecutive colors and return a tuple of consecutive colors with their color
		"""
		Lines: dict = {}
		unique: set = set(
			(x, y, color) for color in colorwithcoords for y in colorwithcoords[color] for x in colorwithcoords[color][y])
		for color in colorwithcoords:
			Lines[color] = {}
			for y in colorwithcoords[color]:
				consecutivePixels: tuple = self.getConsecutivePixels(
					colorwithcoords[color][y])
				unique -= set((i, y, color)
							  for a, b in consecutivePixels for i in range(a, b+1))
				if consecutivePixels:
					Lines[color][y] = consecutivePixels

		Pixels: tuple = sorted(tuple(unique), key=lambda i: (i[2], i[1], i[0]))
		return Pixels, Lines

	def Bot(self, resize=True) -> None:
		print("- DrawBot Started -")
		self.imagename: str = self.Image_Folder + '/' + 'test3.bmp'

		# Starts drawing from your current mouse position on the canvas
		self.x1, self.y1 = pyautogui.position()

		Drawing = Image.open(str(self.imagename))
		Drawing = Drawing.convert('RGB')

		# if image height > 400, resize it to 400 or less
		self.width: int = Drawing.size[0]
		self.height: int = Drawing.size[1]
		if self.height > 400 and resize:
			Drawing = self.resizeImage(self.imagename)
			self.width = Drawing.size[0]
			self.height = Drawing.size[1]
		# Drawing.show()

		Pixels = Drawing.load()
		print("Press Control to Stop at any time")
		print("Image Height: ", self.height)
		print("Image Width: ", self.width)
		print("Resolution: ", self.width * self.height)

		# Gets the pixel data from the image, and formats them into data for the draw bot
		t1 = time.time()
		print("Starting Converting Image to Pixels...")
		self.ColorWithCoords: dict = {color: {} for color in self.Colors}
		for y in range(0, self.height):
			for x in range(0, self.width):
				rgb = Pixels[x, y]
				closest_rgb = self.closest_color(rgb)
				if closest_rgb != self.White:
					self.ColorWithCoords[closest_rgb].setdefault(y, [])
					self.ColorWithCoords[closest_rgb][y].append(x)
		print("Finished Converting Image to Pixels")
		print("Time to Process Image:", time.time() - t1)

		# Optimize the Drawing by removing consecutive pixels and turn them into lines
		t1 = time.time()
		print("Starting Optimization...")
		Pixels, Lines = self.optimize(self.ColorWithCoords)
		print("Finished Optimizing")
		print("Time to Optimize:", time.time() - t1)

		# with open("optimized.txt", "w") as f:
		# f.write(str(Lines))
		oldPixels = sum(sum(len(yDict[y]) for y in yDict)
						for yDict in self.ColorWithCoords.values())
		newPixels = len(Pixels)
		print("Before Optimization:", oldPixels, "Pixels")
		print("After Optimization:", newPixels, "Pixels and", *
			  [sum(len(Lines[b][a]) for b in Lines for a in Lines[b])], "Lines")
		print(
			f"Percentage Decrease in Pixels: {round(((oldPixels - newPixels)/oldPixels)*100, 2)}%")
		# exit()

		time.sleep(2)
		self.Draw(Pixels, Lines)

	def Draw(self, Pixels: Tuple[Tuple[int]], Lines: Dict[tuple, Dict[int, Tuple[Tuple[int]]]]) -> None:
		global break_program
		# Draws Lines
		for Color in Lines:
			if Color != self.SameColor:
				self.SameColor = Color
				self.Change_Color(self.match_color(Color))
			CurrentColor = Lines[Color]
			for y in CurrentColor:
				currentY = Lines[Color][y]
				for x in currentY:
					self.drag(self.x1+x[0], self.x1+x[1], self.y1+y)
					if break_program:
						exit()

		# Draws Pixels
		for pixel in Pixels:
			if pixel[2] != self.SameColor:
				self.SameColor = pixel[2]
				self.Change_Color(self.match_color(pixel[2]))
			self.click(self.x1+pixel[0], self.y1+pixel[1])
			if break_program:
				exit()
		break_program = True

	def calibrate(self) -> None:
		"""
		Function to calibrate the drawing bot colors, or change the color positions,
		in case of different color positions relative to the screen, or
		trying a new sort of drawing application.

		Use:
						Hover over the color you want to add with your mouse,
						then press enter, to move onto the next color, and so on.
						Once you have added all the colors you want, input a single 'x' to finish calibrating.

		Output:
						A dictionary with the color names as keys and the color positions as values.
						Which can be copied and pasted above in the class constants.
		"""
		print("- Calibration Started - Type x to quit inputting colors")
		self.Colors = {}
		while (input() != "x"):
			position = tuple(pyautogui.position())
			screenshot = pyautogui.screenshot()
			color = tuple(screenshot.getpixel(position))[:3]
			print(f"Color: {color}, Position: {position}")
			self.Colors[color] = position
		print(self.Colors)

	def testColorPosition(self):
		for colorPos in self.Colors.values():
			pyautogui.click(colorPos)
			time.sleep(1)


if __name__ == "__main__":
	Bot = DrawBot()
	# Uncomment the line below to calibrate the drawing bot colors if the colors are not in the right position
	Bot.calibrate()
	# Uncomment the line below to test the color positions
	# Bot.testColorPosition()
	Bot.Bot()
	# Bot.calibrate()
