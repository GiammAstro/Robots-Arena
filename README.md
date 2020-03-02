# Robots-Arena
 This is a repo that contains the Robots-Arena project.

 - CONTENT OF THE REPO
 The repo contains:
 1) The ROBOTS-ARENA.py main code, containing the main loop of the game
 2) The game_app.py containing the definition of the "game" class which variables and functions are used in the main function of the game
 3) a "img" folder containing the image that is used by the game as a background for the robots arena
 4) a "robots" folder containing few examples of how to programm your robot AI and a template that can be used to this purpose in the "robots_garage" folder (inside the robots folder).
 5) The project workspace that can be opened with Visual Studio Code

 - HIGH LEVEL ARCHITECTURE

 1) Main function 
 
 The main function "main()" is defined in the "ROBOTS-ARENA.py" file. Most of the functions used in this function are imported from the "game" class, defined in "game_app.py". This function contains the high level logic of the game structured as follows:

-- GAME INITIALIZATION -- 

a) As first action the robots placed in the "robots" folder are loaded and their definition is checked in therms of skills. This is done calling the "import_robots()" function. Only the robots in the folder, and no the one in the "robots_garage" subfolder, are loaded. A maximum of 4 robots can compete on the arena at the same time. If more than 4 robots are defined by the user, the others (which will not be loaded) have to be placed in the "robots_garage2 folder.
    
b) The robots are then placed to their initial position with the function "place_robots()" which is also assigning the initial statistics like health and so on to the robots. In this step basically the robot state is defined. This state will be modified, updated, during the game evolution by other functions. The statistics(status) of the robots are stored in a class dictionary called "robots_stat". This dictionary contains the position of the robots, their health, the information about the shots that have been fired (position, power, direction), the color of the robot (that will be used in the game for showing the marker of the robot in the arena as well as its shots and statistics).

c) The arena and the game window are generated. At this time the internal variables of the "game" class used for monitoring the status of the game (start, pause, quit, reset) are also generated and initialized.

d) The dobots are then plotted in the arena in their initial position assigned at (b). At this point none of the robots has an assigned "marker" object, thus this is generated and placed at the initial robot position with the assigned color.

-- GAME LOOP --

The following actions are repeated in a loop since from this point we want the game to be commanded by the used by clicking on the 4 Start, Quit, Pause and Reset buttons. The loop is executed while there is still time left for the match evolution or there is more than one robot left which means that there no winner.

e) At the beginning of each loop a refresh of the game graphics and internal variables is executed.

f) A check for the internal variable for the "Quit" button is done. In case the button has been pressed the script (the whole game window) is closed.

g) A check for the internal variable for the "Pause" button is done. In case the button has been pressed the script enters in a while loop that is executed until another user input is given. Within this script the game is refreshed for checking the user input.

h) A check for the internal variable for the "Reset" button is done. In case the user wants to reset the game a function for resetting the robots positions and showing them in the arena is called. The "countdown" flag is also set againto true in order to display the countdown in case the user wants to start the game again by pressing the "Start" button.

i) A check for the internal variable for the "Start" button is done. In case the user wants to start the match a sequence of actions is executed: the "animate_match" function is called, the "check_hit" function is called, the robots and the shots are drawn ("draw_robots" and "draw_shots" functions). The aforementioned functions have the following purpose:

i.1) "animate_match" function: this function is called for computing the inputs that are given to the robots AI (position of the robot, and infos about the other robots and shots in the view radius). Once this info is given to the robots AI the function checks for the decisions about direction to move and shots to fire (direction). The function then applies the moves to both the robots and shots.

i.2) "check_hit" function: this function checks for the robots being hit by the shots. In case a robot has been hit the function reduces the value of the health of the robot according to the power of the fired shot and the shield of the hit robot.

i.3) "draw_robots" function: This function already used in (d) draws the robots in their position with a marker color that switches to gray if the robot is dead.

i.4) "draw_shots" function: This function draws the shots of the alive robots showing them on the arena.

At the end of the loop a message is displayed on the screen regarding if there is a winner or not.


The following diagram is showing the aforementioned blocks in the way they are called in the main function:

                                    IMPORT ROBOTS (a)

                                          |
                                          V

                                     PLACE ROBOTS (b)

                                          |
                                          V

                                    GENERATE ARENA (c)

                                          |
                                          V

                                      DRAW ROBOTS (d)

                                          |
                                          V

            >---->------>------>-----> REFRESH GAME (e)
            |
            |                             |
            |                             V
            |
            |                          IF QUIT -- TRUE -- QUITTING THE GAME (f) 
            |
            |                             |
            |                             V
            |
            |                          IF PAUSE -- TRUE -- PAUSING THE GAME (g)
            |
            |                             |
    WHILE TIME != 0 AND NOT WINNER        V
            |
            |                          IF RESET -- TRUE -- RESETTING THE GAME (h)
            |
            |                             |
            |                             V
            |
            |                          IF START -- TRUE -- STARTING AND EVOLVING THE MATCH (i)
            |
            |                             |
            <---<------<-------<-----<----
                                          |
                                          V

                                         END

- COMPILATION AND RUNNING INSTRUCTIONS

-- Compilation --

The code has been developer using python version 3.5.2 and the following libraries:

1) numpy version 1.18.1
2) matplotlib version 2.1.0
3) tkinter version 8.5

-- Running --

In order to run the game the ROBOTS-ARENA.py script has to be run. The robots that will participate to the match have to be placed in the robots folder (a maximum number of 4 robots is allowed). In case more than 4 robots are availavble, the others (except the 4 that are competing) have to be placed in the robots_garage folder placed inside the robots folder. The robots_garage folder also contains a template for the writing of the robots AI.

- RULES AND INSTRUCTIONS OF THE GAME

-- Game Mechanics --

-- Arena layout and characteristics --

-- Robot Capabilities --

-- How to write a robot AI --
