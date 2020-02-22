'''This is the main loop of the Robots Arena app. 
It is in charge of importing the robots that are placed in the robots folder 
and to let them participate to the battle. here all the functions used in the main code are defined in a way 
that they can be easily called and the game dynamics can be easily assembled in the main loop. 
All the game limits, physics and graphics are defined here'''

import os
import sys
import importlib.util
from random import randint
import copy
import numpy as np
import matplotlib.pyplot as plt
import time

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
        self.initial_positions = [(8,8),(92,92),(8,92),(92,8)]
        #dimensions of the arena
        self.arena_x_dim = 100
        self.arena_y_dim = 100
        self.arena_diagonal = np.sqrt((self.arena_x_dim)**2+(self.arena_y_dim)**2)
        #speed limit
        self.speed_limit_scaled = 2.5
        self.speed_limit = self.arena_diagonal * self.speed_limit_scaled / 100
        #size od the robots (in percentage of arena size)
        self.robots_size_scaled = 2.5
        self.robots_size = self.arena_diagonal * self.robots_size_scaled / 100
        #countdown before start of match
        self.countdown = 3
        #match length (in seconds)
        self.match_length = 120
        #skills constraints (new one can be added and will be scanned during the robots importing operation)
        self.skill_points_total_limit = 16 #limit to the sum of all the player skills
        self.skill_points_limit = 10 #limit to the points of a single skill
        #skills scaling
        #game physics
        self.time_step = 1

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
                #checking the robot skill points according to the limits
                if (robot_curr.speed+robot_curr.power+robot_curr.shield+robot_curr.view_radius) > self.skill_points_total_limit:
                    raise ValueError('ERROR: robot %s  exceeds max number of total skill points of %s'%(robot_curr.robot_name, self.skill_points_total_limit))
                if (robot_curr.speed > self.skill_points_limit or robot_curr.speed < 0):
                    raise ValueError('ERROR: robot %s speed skill points out of range [0,%s]'%(robot_curr.robot_name, self.skill_points_limit))
                if (robot_curr.power > self.skill_points_limit or robot_curr.speed < 0):
                    raise ValueError('ERROR: robot %s power skill points out of range [0,%s]'%(robot_curr.robot_name, self.skill_points_limit))
                if (robot_curr.shield > self.skill_points_limit or robot_curr.speed < 0):
                    raise ValueError('ERROR: robot %s shield skill points out of range [0,%s]'%(robot_curr.robot_name, self.skill_points_limit))
                if (robot_curr.view_radius > self.skill_points_limit or robot_curr.speed < 0):
                    raise ValueError('ERROR: robot %s view_radius skill points out of range [0,%s]'%(robot_curr.robot_name, self.skill_points_limit))
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
        '''This function is placing the imported robots in a specified initial position in the arena.
           This position is stored in a dictionary that will contain the current positions 
           of the robots and all their stats, in this way even if the skills change while the robot is playing 
           (trying to cheat) they will not be updated since they were copied in the initialization phase.
           The health of the robot is also given (the same for each robot) in this moment.
        '''
        counter = 0
        for robot in self.robots:
            pos_x, pos_y = self.initial_positions[counter]
            #pos_x = randint(0, self.arena_x_dim)
            #pos_y = randint(0, self.arena_y_dim)
            self.robots_stat[robot.robot_name] = {}
            self.robots_stat[robot.robot_name]['position'] = (pos_x, pos_y)
            self.robots_stat[robot.robot_name]['health'] = 100
            self.robots_stat[robot.robot_name]['shield'] = robot.shield
            self.robots_stat[robot.robot_name]['speed'] = robot.speed
            self.robots_stat[robot.robot_name]['power'] = robot.power
            self.robots_stat[robot.robot_name]['view_radius'] = robot.view_radius
            self.robots_stat[robot.robot_name]['shots'] = []
            self.robots_stat[robot.robot_name]['marker'] = None
            counter += 1
    
    def animate_match(self):
        '''This function is moving the robots according to their decisions. 
           This is done by giving them the current status in therms of other robots in the radius of view
           and positions of the shots in the range of view and asking them what is the next move 
           specified by an angular direction.
           The function also evolves the shots that were fired by the robots that are still alive. 
           If a robot is dead its shots are removed from the arena.
        '''
        #we cycle on each robot asking the new direction
        for robot_focus in self.robots:
            #we only ask to the robots that are still alive
            if self.robots_stat[robot_focus.robot_name]['health'] != None:
                #first we look for nearby robots and shots
                nearby_robots, nearby_shots = self.nearby_objects(robot_focus.robot_name)
                #then we ask the direction to the robot (that is free of chosing it on its own)
                self.robots_stat[robot_focus.robot_name]['direction'] = robot_focus.move(self.robots_stat[robot_focus.robot_name]['position'], nearby_robots, nearby_shots)
                #we ask to the robot also if he wants to shoot
                self.robots_stat[robot_focus.robot_name]['shots'].append(robot_focus.shoot(self.robots_stat[robot_focus.robot_name]['position'], nearby_robots, nearby_shots))
        
        #we check for feasibility of the movement and if possible we apply the movement
        for robot_focus in self.robots_stat:
            #we apply the movement only if the robot is still alive
            if self.robots_stat[robot_focus]['health'] != None:
                self.robots_stat[robot_focus]['position'] = self.apply_move(robot_focus)
        
        return True

    #-------------UTILITY FUNCTIONS------------------#

    def apply_move(self, robot_name):
        '''This function is in charge of applying the movement to the robot, if it wants to, 
        only is this move is allowed. Moving out of the arena or through another robot is not allowed. 
        Each robot has a radius that determines its dimension and is scaled 
        according to the arena size (it is given in percentage). 
        The same happen for the velocity sckill which is rescaled according to the arena size (in principle a velocity skill)
        '''
        #scaling the velocity skill according to arena dimension
        velocity = self.robots_stat[robot_name]['speed'] /10 * self.speed_limit 
        print(velocity)

        #first we check if the robot wants to move (if it does not want will give a direction of None)
        if self.robots_stat[robot_name]['direction'] != None:
            #if the robot wants to move we compute the expected final position
            shift_x = velocity * np.cos(np.radians(self.robots_stat[robot_name]['direction']))
            shift_y = velocity * np.sin(np.radians(self.robots_stat[robot_name]['direction']))
            exp_final_pos_x = self.robots_stat[robot_name]['position'][0] + shift_x
            exp_final_pos_y = self.robots_stat[robot_name]['position'][1] + shift_y
            #whe check if the final position is out of the arena
            if exp_final_pos_x > (self.arena_x_dim - self.robots_size) :
                final_pos_x = self.arena_x_dim - self.robots_size
            elif exp_final_pos_x < self.robots_size:
                final_pos_x = self.robots_size
            else:
                final_pos_x = exp_final_pos_x
            if exp_final_pos_y > (self.arena_y_dim - self.robots_size) :
                final_pos_y = self.arena_y_dim - self.robots_size
            elif exp_final_pos_y < self.robots_size:
                final_pos_y = self.robots_size
            else:
                final_pos_y = exp_final_pos_y
            #we then check if the final position means a collision with other robots
            for robot in self.robots_stat:
                #we ignore the focused robot
                if robot != robot_name and self.robots_stat[robot]['health'] != None:
                    #we check the distance with the selected robot
                    distance = self.distance((final_pos_x, final_pos_y), self.robots_stat[robot]['position'])
                    if distance < self.robots_size*2:
                        #if moving the robot to the expected positon generates a collision we leave it where it is
                        return self.robots_stat[robot_name]['position']        
            return (final_pos_x, final_pos_y)

        #if the robot does not want to move we leave it there
        else:  
            return self.robots_stat[robot_name]['position']

    def distance(self, p1, p2):
        a = np.array(p1)
        b = np.array(p2)
        dist = np.linalg.norm(a-b)
        return dist
    
    def nearby_objects(self, robot_focus):
        nearby_robots = {}
        nearby_shots = {}
        #first considering the other robots
        for robot in self.robots_stat:
            #ignoring the considered robot
            if robot != robot_focus and self.robots_stat[robot]['health'] != None:
                #selecting robots in radius of view
                if self.distance(self.robots_stat[robot_focus]['position'], self.robots_stat[robot]['position']) <= self.robots_stat[robot_focus]['view_radius']:
                    nearby_robots[robot] = {'pos': self.robots_stat[robot]['position']}
                #selecting shots in radius of view
                for shot_focus in self.robots_stat[robot]['shots']:
                    if shot_focus != None:
                        if self.distance(self.robots_stat[robot_focus]['position'], shot_focus['pos']) <= self.robots_stat[robot_focus]['view_radius']:
                            nearby_shots[robot] = {'pos': shot_focus['pos'], 'dir': shot_focus['dir'], 'power': shot_focus['power']}
        return nearby_robots, nearby_shots

    #--------------GRAPHICAL FUNCTIONS-----------------#
    
    def generate_arena(self): 
        #reading the image that has to be used as arena background
        img = plt.imread("img/robot_wars_arena.jpg")
        #generating the arena figure and axes
        self.fig = plt.figure(figsize=(7,7))
        self.ax = self.fig.add_subplot(111)
        #placing the arena image as background
        self.ax.imshow(img, zorder=0, extent=[1.0, self.arena_x_dim, 1.0, self.arena_y_dim])
        plt.draw()
        plt.pause(2)
        return True
    
    def display_countdown(self):
        #placing the current number of the countdown in the centre of the arena
        for i in range(0, self.countdown + 1):
            #if the countdown did not started yet we have to place the first number in the arena
            if i==0:
                countdown_obj = self.ax.annotate('%s' %(self.countdown - i), (50, 50),
                fontsize=60, horizontalalignment='center', verticalalignment='center', color='red')
            #if the countdown already started we have only to update the text of the annotation
            #if we reached the end of countdown we display a message
            elif i == self.countdown:
                countdown_obj.set_text('GO!!')
            else:
                countdown_obj.set_text('%s' %(self.countdown - i))
            plt.draw()
            plt.pause(1)
        #at the end of the countdown after the message has been displayed we remove it and the match starts
        countdown_obj.remove()
        plt.draw()
        
    
    def draw_robots(self):
        #placing the robots in the arena
        for robot in self.robots_stat:
            if self.robots_stat[robot]['health'] != None:
                if self.robots_stat[robot]['marker'] in self.ax.artists:
                    self.ax.artists.remove(self.robots_stat[robot]['marker'])
                    self.robots_stat[robot]['marker'].center = (self.robots_stat[robot]['position'])
                else:
                    self.robots_stat[robot]['marker'] = plt.Circle(self.robots_stat[robot]['position'], self.robots_size, color='blue')
                self.ax.add_artist(self.robots_stat[robot]['marker'])
            else:
                self.ax.artists.remove(self.robots_stat[robot]['marker'])
        plt.draw()
        plt.pause(0.001)
        return True
