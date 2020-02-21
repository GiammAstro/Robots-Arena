'''This is the main loop of the Robots Arena app. 
It is in charge of importing the robots that are placed in the robots folder 
and to let them participate to the battle.'''

import os
import sys

class game:

    def __init__(self):
        #folder where the robots are placed
        self.importing_folder = 'robots'
        sys.path.insert(1, 'robots/')
        #defining the robots list as empty
        self.robots = []
        #players that participate to a match
        self.max_player_number = 4
        #dimensions of the arena
        self.arena_x_dim = 40
        self.arena_y_dim = 40
        #skills constraints (new one can be added and will be scanned during the robots importing operation)
        skills_limit = 16 #limit to the sum of all the player skills
        #skills scaling
        #game physics
        time_step = 1

    def import_robots(self):
        #here we create a list of python files in the robots folder
        robot_list = [x for x in os.listdir(self.importing_folder) if x.endswith('.py')]
        #if there are no robots we raise an error
        if len(robot_list) == 0:
            raise ValueError('ERROR: no robot has been found in the robots folder. Place your robot there and let it win!')
        #if the number of robots does not exceed the maximum allowed players number we proceed
        elif len(robot_list) <= self.max_player_number:
            for robot_file in robot_list:
                robot_class = __import__(robot_file)
                self.robots.append(robot_class.robot())
            print('Selected players %s' %(' '.join(robot_list)))
        #if the number of imported robots exceed the number of maximum players we raise an error
        else:
            raise ValueError('ERROR: number of robots exceeds maximum number of %s participants' %(self.player_number))
        return True

    """ def battle:

        while self.alive_players > 1: """


#----------------MAIN---------------------
game = game()
game.import_robots()