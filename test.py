from labyrinthe import *
from tkinter import mainloop, filedialog

#level = [
#	[(10, 10, 40, 40), "rect", "Start"],
#	[(40, 10, 520, 50, 520, 300, 200, 590, 200, 540, 500, 220, 500, 70, 40, 40), "polygon", "Simple"],
#	[(500, 240, 500, 280, 400, 380), "polygon", "Bad"],
#	[(150, 540, 200, 590), "rect", "Goal"],
#]

level = filedialog.askopenfilename()

if level:
	jeu = Game(800, 600, level)
	mainloop()
else:
	print("Invalid file")
