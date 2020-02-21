'''This is the main loop of the Robots Arena app. 
It is in charge of importing the robots that are placed in the robots folder 
and to let them participate to the battle.'''

import os
import sys
import importlib.util
from random import randint
import copy

class game:

    def __init__(self):
        #folder where the robots are placed
        self.importing_folder = 'robots'
        #defining the robots list as empty
        self.robots = []
        #defining the dictionary containing the robot statuses
        self.robots_stat = {}
        #players that participate to a match
        self.max_player_number = 4
        #dimensions of the arena
        self.arena_x_dim = 100
        self.arena_y_dim = 100
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
                spec = importlib.util.spec_from_file_location("robots.%s" %robot_file, "%s/%s" %(self.importing_folder, robot_file))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                robot_curr = foo.robot()
                print('imported robot %s' %(robot_curr.robot_name))
                self.robots.append(robot_curr)
            print('Selected players %s' %(' '.join(robot_list)))
        #if the number of imported robots exceed the number of maximum players we raise an error
        else:
            raise ValueError('ERROR: number of robots exceeds maximum number of %s participants' %(self.player_number))
        return True

    #def battle:

        #while self.alive_players > 1:
    
    def place_robots(self):
        '''This function is placing the imported robots in a randomic initial position in the arena.
           This position is stored in a dictionary that will contain the current positions 
           of the robots and all their stats, in this way even if the skills change while the robot is playing 
           (trying to cheat) they will not be updated since they were copied in the initialization phase.
           The health of the robot is also given (the same for each robot) in this moment.
        '''
        for robot in self.robots:
            pos_x = randint(0, self.arena_x_dim)
            pos_y = randint(0, self.arena_y_dim)
            self.robots_stat[robot.robot_name] = {}
            self.robots_stat[robot.robot_name]['position'] = (pos_x, pos_y)
            self.robots_stat[robot.robot_name]['health'] = 100
            self.robots_stat[robot.robot_name]['shield'] = robot.shield
            self.robots_stat[robot.robot_name]['speed'] = robot.speed
            self.robots_stat[robot.robot_name]['power'] = robot.power
            self.robots_stat[robot.robot_name]['view_radius'] = robot.view_radius
    
    def move_robots(self):
        '''This function is moving the robots according to their decisions. 
           This is done by giving them the current status in therms of other robots in the radius of view
           and positions of the shots in the range of view and asking them what is the next move 
           specified by an angular direction.
        '''
        self.robots_stat_old = copy.deepcopy(self.robots_stat)
        for robot in self.robots:
            
            direction = robot.move(self.robots_stat_old[robot.robot_name]['position'], )
            self.robots[]

#----------------MAIN---------------------
game = game()
game.import_robots()
game.place_robots()