from tkinter import Tk, Canvas, Label
import time
from level_parser import *

FILL_BG = "#980000"
FILL_FG = "#ffe8a0"
FILL_GOAL = "#004890"
FILL_START = "#009000"
FILL_NEUTRAL = "#b0b0b0"

class Game:
	def __init__(self, W, H, levelfile):
		master = Tk()
		text = Label(master, font=("Georgia", 20, "bold"), text="Loading...")
		text.pack()
		canvas = Canvas(master, width=W, height=H, bg=FILL_NEUTRAL)
		canvas.pack()
		canvas.bind("<Motion>", self.update)
		canvas.bind("<Button-1>", self.click)
		levels = parse_file(levelfile)
		self.levels = []
		for level in levels:
			self.levels.append(Level(level))
		self.nlevel = 0
		self.current_level = self.levels[0]
		text.config(text=self.current_level.name)
		self.text = text
		self.canvas = canvas
		self.playing = False
		self.W = W
		self.H = H
		self.display()

	def increment_level(self):
		n = (self.nlevel + 1) % len(self.levels)
		self.nlevel = n
		self.current_level = self.levels[n]
		self.text.config(text=self.current_level.name)

	def display(self):
		canvas = self.canvas
		canvas.delete("all")
		self.current_level.display(canvas, self.playing)
		canvas.update()

	def update(self, event):
		if not self.playing:
			return
		canvas = self.canvas
		pos = (event.x, event.y)
		zone = self.current_level.get_zone(pos)
		if zone == "bad":
			self.playing = False
			canvas.delete("all")
			canvas.config(background=FILL_NEUTRAL)
			canvas.create_text((self.W / 2, self.H / 2), font=("Georgia", 40, "bold"), text="Perdu !", fill=FILL_BG)
			canvas.update()
			time.sleep(1)
			self.display()

	def click(self, event):
		canvas = self.canvas
		pos = (event.x, event.y)
		zone = self.current_level.get_zone(pos)
		if self.playing:
			if zone == "goal":
				self.playing = False
				text = "Gagné !"
				win = self.nlevel + 1 == len(self.levels)
				if win:
					text = "Gagné à tous les niveaux !"
				canvas.delete("all")
				canvas.config(background=FILL_NEUTRAL)
				canvas.create_text((self.W / 2, self.H / 2), font=("Georgia", 40, "bold"), text=text, fill=FILL_GOAL)
				canvas.update()
				time.sleep(1)
				self.increment_level()
				self.display()
		else:
			if zone == "start":
				self.playing = True
				canvas.delete("all")
				canvas.config(background=FILL_BG)
				self.display()

class Level:
	def __init__(self, element):
		self.name, ground_list = parse_level(element)
		self.grounds = []
		for ground in ground_list:
			self.grounds.append(Ground(ground))

	def display(self, canvas, playing):
		for ground in self.grounds:
			ground.display(canvas, playing)

	def get_zone(self, pos):
		for ground in reversed(self.grounds): # Iterate from the foreground to the background
			if ground.contains(pos):
				return ground.properties
		return "bad" # If not in any zone, bad zone.

def is_in_rectangle(pos, bbox):
	return pos[0] >= bbox[0] and pos[1] >= bbox[1] and pos[0] <= bbox[2] and pos[1] <= bbox[3]

def is_in_oval(pos, center, radius):
	return ((pos[0] - center[0])/radius[0]) ** 2 + ((pos[1] - center[1])/radius[1]) ** 2 <= 1

def is_in_polygon(c, vert, bbox, pts): # c is pos
	if not is_in_rectangle(c, bbox): # If c is not in the bounding box of the polygon, it can't be inside.
		return False

	# Algorithm: the point c is in the polygon if it intersects an odd number of segments. Borders are considered to be inside the polygon.

	is_inside = False
	for i in range(pts):
		if i == 0:
			a = (vert[2*pts-2], vert[2*pts-1])
		else:
			a = (vert[2*i-2], vert[2*i-1])

		b = (vert[2*i], vert[2*i+1])

		if b == c:
			return True # On a point

		# Now find whether [ab] cuts the vertical half-line [cy), so whether [ab] is above c

		if a[0] > b[0]:
			a, b = b, a # Reverse the order: b[0] should be bigger than a[0]

		if a[0] > c[0] or b[0] <= c[0]: # a and b are on the same side, they can't intersect [cy)
			if a[0] == c[0] and (a[1]-c[1])*(b[1]-c[1]) <= 0: # exception: if a and b are on a vertical line that contains c
				return True # On the border
			continue

		d = (b[0]-c[0])*(a[1]-c[1])-(a[0]-c[0])*(b[1]-c[1]) # Positive if [ab] is above point c

		if d == 0:
			return True # On the border

		if d > 0:
			is_inside = not is_inside # Invert is_inside. The point is inside the polygon if the number of segments intersected by [cy) is an odd number.
	return is_inside

class Ground:
	def __init__(self, element): # vertices, shape="rect", animation=None, properties="Simple", active=True):
		vertices, shape, properties, animation, active=parse_ground(element)
		self.shape = shape
		self.vert = vertices
		self.active = active
		if not animation:
			self.animated = False
		else:
			self.anim = animation
			self.animated = True
		self.properties = properties
		if shape == "oval":
			center = ((vertices[0]+vertices[2])/2, (vertices[1]+vertices[3])/2)
			self.center = center
			self.radius = (center[0]-vertices[0], center[1]-vertices[1])
		elif shape == "polygon":
			bbox = [vertices[0], vertices[1], vertices[0], vertices[1]]
			self.points = len(vertices) // 2
			for i in range(1, self.points):
				x = vertices[2*i]
				y = vertices[2*i+1]
				if x < bbox[0]:
					bbox[0] = x
				elif x > bbox[2]:
					bbox[2] = x
				if y < bbox[1]:
					bbox[1] = y
				elif y > bbox[3]:
					bbox[3] = y
			self.bbox = tuple(bbox)

	def display(self, canvas, playing):
		if not self.active:
			return

		vert = self.vert
		color = FILL_NEUTRAL
		if playing:
			if self.properties == "simple":
				color = FILL_FG
			elif self.properties == "bad":
				color = FILL_BG
			elif self.properties == "goal":
				color = FILL_GOAL
			elif self.properties == "start":
				color = FILL_START
		else:
			if self.properties == "start":
				color = FILL_START

		if self.animated:
			vert = self.anim.move(vert)

		if self.shape == "rect":
			canvas.create_rectangle(vert, fill=color, outline="black")
		elif self.shape == "oval":
			canvas.create_oval(vert, fill=color, outline="black")
		elif self.shape == "polygon":
			canvas.create_polygon(vert, fill=color, outline="black")

	def contains(self, pos):
		if not self.active:
			return False

		if self.shape == "rect":
			return is_in_rectangle(pos, self.vert)
		elif self.shape == "oval":
			return is_in_oval(pos, self.center, self.radius)
		elif self.shape == "polygon":
			return is_in_polygon(pos, self.vert, self.bbox, self.points)
