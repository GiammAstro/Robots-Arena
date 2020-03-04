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
 
 The main function "main()" is defined in the "ROBOTS-ARENA.py" file. Most of the functionalities used in this function are imported from the "game" class, defined in "game_app.py". This function contains the high level logic of the game structured as follows:

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

                                    SHOW RESULT

                                          |
                                          V

                                         END


- COMPILATION AND RUNNING INSTRUCTIONS

-- Compilation --

The code has been developer using python version 3.5.2 and the following libraries:

1) numpy version 1.18.1
2) matplotlib version 2.1.0
3) tkinter version 8.5

Since python is not a compiled language, once the user is sure to have the available used libraries he will be able to run the game.

-- Running --

In order to run the game the ROBOTS-ARENA.py script has to be run. The robots that will participate to the match have to be placed in the robots folder (a maximum number of 4 robots is allowed). In case more than 4 robots are availavble, the others (except the 4 that are competing) have to be placed in the robots_garage folder placed inside the robots folder. The robots_garage folder also contains a template for the writing of the robots AI.

- RULES AND INSTRUCTIONS OF THE GAME

-- Game Mechanics --
The game is structure in a way that the complete evolution of the match can be summarized in the following list of actions:

1) robot movement: a robot can move inside the arena and is asked for which direction it wants to move according to the velocity that is specified in the robot definition file (the robot AI python code). A robot cannot move out of the arena and is only asked for the direction. The movement itself is applied by the game loop and the final position of the robot is generated in the game loop. A robot can never impose its final position but only suggest to the game in which direction it would like to move.

2) shots evolution: each robot is asked once every 2 seconds if it wants to fire a shot and in which direction. The will to fire and the direction are chosen by the robot according to its AI. The game will then evolve the position of the shots in the arena until they move out of it or hit another robot. In both cases the interested shot is deleted from the arena. 

3) hit checking: at every game cycle a check for the shot-robot hit is performed. In case a hit is verified the effects of the event on the interested robot and shot are applied. The health of the robot is decreased according to the power of the shot and the shielding of the robot, and set to None in case it goes below or equal to zero. The interested shot is deleted from the arena once the hit has been validated. The game will check for hits only in the nearby shots list which contains the list of shots that are in the radius of view of each robot.

-- Arena layout and characteristics --
The arena has a square shape and a fixed dimension. The robots start their match from the four corners of the arena and cannot navigate outside of the arena. Each physical dimension such as robot size or velocity is scaled according to the dimension of the area. The robot size is predefined and equal for each robot and a robot cannot occupy a position that is closer than the robot dimension to the border of the arena. Each robot is free of moving in whatever direction it wants and is asked for the direction of movement and the firing of the shots at every game cycle. Once a shot exits the arena it is deleted as well as once a robot tries to exit the arena only the velocity component that is parallel to the arena border will be applied to the movement making the robot look like it is sliding along the border.

-- Robot Capabilities --
Each robot has the capability of moving inside the arena and shooting. Both actions require a direction that is chosen by the robot according to its AI. Given a robot and its radius of view it will receive as input the informations about the robots and the shots coming from those robots that are in this radius. The robot can not know or observe objects that are out of its radius of view. At the beginning of the match every robot receives 100 health points and the damage effect caused by being hit by a shot is determined according to the robot shield and the power of the shot that has been fired from another robot.

-- How to write a robot AI --
Each robot is defined as a python class that is imported when the robots are loaded. Inside the class there are 3 functions that the user can program:

1) "skills" function: this function contains the 4 robot skills that can be set using a total of 16 skill points with a maximum of 10 points per each skill. The skills are "speed", "power", "view_radius" and "shield".

            def skills(self):
                  '''In this function you can define the 4 skills of your robot which are:
                        1) the speed "self.speed"
                        2) the shooting power "self.power"
                        3) the view radius "self.view_radius"
                        4) the shield of the robot "self.shield"
                        
                        REMEMBER: you have a maximum of 16 robot skill points to give to your robot. 
                        A higher total number of skill points is not accepted. Each skill can have a maximum of 10 points
                        so as example a speed of 11 or 16 is not allowed.
                  '''
                  self.speed = 0
                  self.power = 0
                  self.view_radius = 0
                  self.shield = 0
                  return True

1.1) The "speed" defines how fast can the robot move. The higher the speed is the faster the robot will move. By chosing a speed of 0 the user will be able to create a robot that does not move at all.

1.2) The "power" defines how much damage does a shot that is fired from the robot cause when it hits another robot. On a scale from 0 to 10 a power of 0 will casue a minimum (not null) damage to the robot, while a power of 10 will cause the maximum damage possible.

1.3) The "view_radius" defiens how far the robot can see. Only the objects inside this radius will be transmitted to the robot as input (hence seen by it). Those are the only elements the robot AI can base on for computing its next move.

1.4) The "shield" skill defines how muche the power of the shot that hits the robot is damped. In fact the computation for the damage of a shot is done considering both the shield of the hit robot and the power of the one that fired the shot.

2) "move" function: this function receives as input the position of the robot specified in the "__pos" tuple and the position of the nearby robots and shots given in the two dictionaries "__players_in_radius" and "__shots_in_radius". The output of the function has to be given in the form of angular direction of movement in degrees. The algorithm inside the function has to be implemented by the user in order to decide how the robot should behave basing on the input information.

            def move(self, __pos, __players_in_radius, __shots_in_radius):
                  ''''Here you can chose how you want your robot to move in the arena,
                        basing on the information that you have.
                        
                        INPUT:
                        1) position of the robot stored in the "position" variable and given as a tuple (x,y)
                        2) position of the other robots in the view radius as tuple (x,y) 
                        accessible by "position" property of "robots_in_radius" dictionary objects
                        structured as follows:
                              robots_in_radius = {
                                    $robot_name_1: {position: (x1,y1)},
                                    $robot_name_2: {position: (x2,y2)},
                                    ...
                                    $robot_name_n: {position: (xn,yn)},
                              }
                        3) position, direction, power and distance of the shots in the view radius given as:
                        - a tuple for the "position" property (x,y)
                        - an integer for the "direction" property of the shots given in degrees
                        - and integer for the "power" of the shots
                        accessible from the "shots_in_radius" dictionary objects 
                        structured as follows:
                              shots_in_radius = {
                                          $robot_name_1: [[{position: (x_1_1,y_1_1), direction: dir_1_1, power:pow_1_1}, distance],
                                                            {position: (x_1_2,y_1_2), direction: dir_1_1, power:pow_1_2},
                                                            ...
                                                            {position: (x_1_n,y_1_n), direction: dir_1_n, power:pow_1_n}
                                          ],
                                          $robot_name_2: [{position: (x_2_1,y_2_1), direction: dir_2_1, power:pow_2_1},
                                                            {position: (x_2_2,y_2_2), direction: dir_2_1, power:pow_2_2},
                                                            ...
                                                            {position: (x_2_n,y_2_n), direction: dir_1_n, power:pow_2_n}
                                          ],
                                          ...,
                                          $robot_name_m: [{position: (x_m_1,y_m_1), direction: dir_m_1, power:pow_m_1},
                                                            {position: (x_m_2,y_m_2), direction: dir_m_1, power:pow_m_2},
                                                            ...
                                                            {position: (x_m_n,y_m_n), direction: dir_m_n, power:pow_m_n}
                                          ],
                                          
                              }
                        
                        OUTPUT: Basing on the information you have and on the speed that you selected in your robot skills
                        you have to consider how you want to move your robot. You can implement your own logic 
                        for chosing how your robot should behave but the output has to be given  in the form of:
                        1) the movement direction expressed in the form of the angular direction in the field 
                        (clockwise from the orizontal right direction, corresponding to the positive x axis) given in degrees. 
                        If no direction is given ("direction" = None) the robot will stand still
                  '''
                  direction = None
                  return direction

3) "shoot" function: this function receives the same inputs as the "move" function. The output of the function has to be given in the form of angular direction of the fired shot in degrees. The algorithm inside the function has to be implemented by the user in order to decide how the robot should behave basing on the input information. Every two seconds the outputted shot will be accepted by the game and plotted on the arena.

            def shoot(self, __pos, __players_in_radius, __shots_in_radius):
                  '''Here you can chose how you want your robot to shoot in the arena,
                        basing on the information that you have.
                        
                        INPUT:
                        1) position of the robot stored in the "position" variable and given as a tuple (x,y)
                        2) position of the other robots in the view radius as tuple (x,y) 
                        accessible by "position" property of "robots_in_radius" dictionary objects
                        structured as follows:
                              robots_in_radius = {
                                    $robot_name_1: {position: (x1,y1)},
                                    $robot_name_2: {position: (x2,y2)},
                                    ...
                                    $robot_name_n: {position: (xn,yn)},
                              }
                        3) position and direction and power of the shots in the view radius given as:
                        - a tuple for the "position" property (x,y)
                        - an integer for the "direction" property of the shots given in degrees
                        - and integer for the "power" of the shots
                        accessible from the "shots_in_radius" dictionary objects 
                        structured as follows:
                              shots_in_radius = {
                                          $robot_name_1: [{position: (x_1_1,y_1_1), direction: dir_1_1, power:pow_1_1},
                                                            {position: (x_1_2,y_1_2), direction: dir_1_1, power:pow_1_2},
                                                            ...
                                                            {position: (x_1_n,y_1_n), direction: dir_1_n, power:pow_1_n}
                                          ],
                                          $robot_name_2: [{position: (x_2_1,y_2_1), direction: dir_2_1, power:pow_2_1},
                                                            {position: (x_2_2,y_2_2), direction: dir_2_1, power:pow_2_2},
                                                            ...
                                                            {position: (x_2_n,y_2_n), direction: dir_1_n, power:pow_2_n}
                                          ],
                                          ...,
                                          $robot_name_m: [{position: (x_m_1,y_m_1), direction: dir_m_1, power:pow_m_1},
                                                            {position: (x_m_2,y_m_2), direction: dir_m_1, power:pow_m_2},
                                                            ...
                                                            {position: (x_m_n,y_m_n), direction: dir_m_n, power:pow_m_n}
                                          ],
                                          
                              }               
                        
                        OUTPUT: Basing on the information you have and on the power that you selected in your robot skills
                        you have to consider how you want to shoot. You can implement your own logic 
                        for chosing how your robot should behave but the output has to be given  in the form of:
                        1) the direction of the shots expressed in the form of the angular direction in the field 
                        (clockwise from the orizontal right direction, corresponding to the positive x axis) given in degrees. 
                        If no direction is given ("shot" = None) the robot will not shoot
                  '''
                  self.shot = None
                  return self.shot

Inside the given functions the user that is programming the AI can insert his own logic to generate di directional angles of both the movement and the fired shot.

- COMMENTS

-- Current implementation tradeoffs
The current status of the code is mainy limited by the graphical library (matplotlib) used for representing the arena. This library slows down the generation of the arena status but on the contrary it can be implemented faster. With a few lines of code it is possible to generate an object in the arena and animate it (making it move) just by updating its coordinates property and refreshing the graph. Nevertheless, matplotlib was not designed as a graphical engine to be implemented in videogames, even if its simplicity makes it extremely scalable.
A second tradeoff is represented by the necessity of calling the "refres_game" at every game cycle. If this function is not called the user given input will not have any effect on the game as the internal variable that is set by the function called by the pressing of the button will not be changed. This happens since the pressing of a button is an event in Tkinter, and this event is only registered once if the log of the events is not refreshed by giving the "self.root.update()" command contained in the "refresh_game" function. At the same time this leaves to the developer the possibility to chose when to accept user external inputs only when ready to react to them.
Another tradeoff is represented by the number of players allowed to participate in a match. This number in fact is fixed to four. This choice has been mainly driven by the selected arena geometry (squared). This geometry makes it easier to constrain the robots inside the arena and to compute if a shot is inside/outside of the playing field. At the same time if the initial position fo the robots has not to be set randomically, to avoid unfair situations in case some robots are generate closer to each other respect to other ones, a natural choice is to place them at the corners of the arena, hence a maximum of four players will be allowed.

-- Implementing new features
The code is compartmentalized in a way that implementing new features is easy and fast. All the informations about the robots and shots is contained in a dictionary of the "game" class. tThe same dictionary also contains the graphical objects (markers) that are modified and updated in case the position is changed. Since every class function can access this dictionary it is easy to implement new functionalities and the developer should only worry about the correct moment for calling these functions in the main loop of the game.

-- Things to improve
The graphical part could certainly be improved trying to optimize the refreshing of the game window and of the arena. This task requires more research and possibly the implementation fo a different library for generating the arena image and plotting the robots and shots markers in it.
A second improvement could regard the features given to the user that programs the robots AI. In fact the freedom of chosing of the robot marker color, or the customization of the robot icon in the arena, could be given to the user. This would require a predefinition of a set of icons, that will then be placed in the arena instead of the standard circular marker.
Always regarding the marker, an indication of the heading of the robot could be added to the marker, to let the players know in which direction is their robot moving.
You will notice that the arena background image is inspired by the show Robot-Wars. Different traps and special rules where applied to precise areas of the arena in the show. This arena features could be implemented in the ROBOTS-ARENA game too toghether with some other basic functionalities like the bouncing back of the robots once they reache the border of the arena, or the damage if tho robots collide.
A last but not least improvement could be to migrate the entire code in a docker container, in order to provide the final user (who has installed docker) a working code with all the related libraries without the need of installing anything. Nevertheless the docker solution is usually applied to numerical algorithms that do not include a graphical UI. This is not the case and applying this solution may require time as the standard video output of the virtual machine that runs in the dockerized container will have to be recognized as the user screen.

-- Robots example
In the "robots" folder three examples of robot AI are placed:

1) "robot_A.py" is the first robot that is programmed to move with a constant direction and fire in the same direction. The chosen direction is 45 degrees.

2) "robot_B.py" is the second robot example, this robot stands still in the initial position without moving and firing. This is for proving that in order to skip the movement and firing actions a None value for both direction and shot values has to be given

3) "robot_C.py" is the third example of a robot AI. This robot is programmed for reaching the centre of the arena as fast as possible (hence it will have a high speed skill) and from there fire in the direction of the nearby robots (this is also the reason why it has a higher radius of view)