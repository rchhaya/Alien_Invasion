# Alien_Invasion
A Space Invaders-type game created using PyGame

This is an adaptation of Space Invaders that was created with guidance from "Python Crash Course" by Eric Matthes.
The basic functions of the aliens and bullets exist in the Aliens and Bullets class, respectively. The game functions, like checking for events, checking for collisions,
and updating various game components, exist in the Alien_Game_Functions.py file. The actual gameplay is handled in the Alien_Invasion.py file. This file contains some classes 
for the game settings, statistics, buttons, and ships. It also contains the game initialization and the game loop.

Regarding the actual game, the user controls the spaceship using left and right arrow keys. To shoot, the user should press the space button. The goal of the game is 
to shoot amd kill all of the alien UFOs before they move down and hit you. If you kill all of the aliens, you go the next level and the game gets harder (the aliens move faster). 
If the aliens hit you, the game resets at the current level and a life is deducted from the user. Once all 3 lives are used up, the game is over. 
Note that the user can't shoot more than 5 bullets at a time.
If the current score is the high score of the game (does not carry over when closing/restarting the game), the high score is changed to the current score. This means that the 
first run of the game will result in a high score, assuming the user gets a score higher than 0.

Enjoy!
