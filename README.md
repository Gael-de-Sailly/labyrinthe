# labyrinthe
Projet Python proposé par le professeur de maths / Python project proposed by the maths teacher

**To launch the game:** run the file `launcher.py`, with Python 3 (for exemple typing in a console `python3 path/of/labyrinthe/launcher.py`)

1) At the start of Labyrinthe, you must provide an xml file with game levels.
You can use `levels/default_levels.xml` file, that holds 5 levels

2) Once levels are loaded, the first level appears and the game starts.

Starting from a green zone, you have to tread through yellow, without ever touching red, to reach the blue zone

The action starts with a left click on the green zone and ends : 
- with failure if the mouse touches red. Then the action restarts on the same level.
- with success if you manage to left-click on the blue zone. Then you either go to the next level, if there is one, or you finish the game.

## Todo list
* Suport for animation
* Interactive zones (zones that once clicked, will start an animation or make another zone appear)
* Level editor ? (much more difficult)
* Settings for colors
