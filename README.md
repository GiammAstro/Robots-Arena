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
    
a) As first action the robots placed in the "robots" folder are loaded and their definition is checked in therms of skills. This is done calling the "import_robots()" function. Only the robots in the folder, and no the one in the "robots_garage" subfolder, are loaded. A maximum of 4 robots can compete on the arena at the same time. If more than 4 robots are defined by the user, the others (which will not be loaded) have to be placed in the "robots_garage2 folder.
    
b) The robots are then placed to their initial position with the function "place_robots()" which is also assigning the initial statistics like health and so on to the robots. In this step basically the robot state is defined. This state will be modified, updated, during the game evolution by other functions. The statistics(status) of the robots are stored in a class dictionary called "robots_stat". This dictionary contains the position of the robots, their health, the information about the shots that have been fired (position, power, direction), the color of the robot (that will be used in the game for showing the marker of the robot in the arena


                                    IMPORT ROBOTS (a)
                                          |
                                          |
                                     PLACE ROBOTS (b)
                                          |
                                          |
                                    GENERATE ARENA (c)
                                          |
                                          |
                                      DRAW ROBOTS (d)
                                          |
                                          |
                                      REFRESH GAME (e)
                                          |
                                          |
            -------------------------- IF QUIT -- TRUE -- QUITTING THE GAME (f) 
            |                             |
            |                             |
            |                          IF PAUSE -- TRUE -- PAUSING THE GAME (g)
            |                             |
WHILE TIME != 0 OR WINNER                 |
            |                          IF RESET -- TRUE -- RESETTING THE GAME (h)
            |                             |
            |                             |
            |                          IF START -- TRUE -- STARTING AND EVOLVING THE MATCH (i)