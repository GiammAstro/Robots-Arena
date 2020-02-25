'''This is the main loop of the Robots Arena app. 
It is in charge of importing the robots that are placed in the robots folder 
and to let them participate to the battle. here all the functions used in the main code are defined in a way 
that they can be easily called and the game dynamics can be easily assembled in the main loop. 
All the game limits, physics and graphics are defined here'''

import os
import sys
import importlib.util
import copy
import numpy as np
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time


class game:

    def __init__(self, fps, match_length):
        #match length
        self.match_length = match_length
        #folder where the robots are placed
        self.importing_folder = 'robots'
        #defining the dictionary containing the robot statuses
        self.robots_stat = {}
        #players that participate to a match
        self.max_player_number = 4
        self.initial_positions = [(8,8),(92,92),(8,92),(92,8)]
        self.robot_colors = ['blue', 'magenta', 'orange', 'green']
        #dimensions of the arena
        self.arena_x_dim = 100
        self.arena_y_dim = 100
        self.arena_diagonal = np.sqrt((self.arena_x_dim)**2+(self.arena_y_dim)**2)
        #frames per second
        self.fps = fps
        #shoot frequency (shoots per second, minimum is 1)
        self.shooting_freq = 0.8
        self.shooting_time = 0
        #robot speed limit
        self.speed_limit_scaled = 15 * (60/self.fps) / 1000
        self.speed_limit = self.arena_diagonal * self.speed_limit_scaled
        #shots speed
        self.speed_shot_scaled = self.speed_limit_scaled*2
        self.speed_shot = self.arena_diagonal * self.speed_shot_scaled
        #size od the robots (in percentage of arena size)
        self.robots_size_scaled = 2.5
        self.robots_size = self.arena_diagonal * self.robots_size_scaled /100
        #size of the shots
        self.shot_size = self.robots_size / 10
        #countdown before start of match
        self.countdown = 3
        #skills constraints (new one can be added and will be scanned during the robots importing operation)
        self.skill_points_total_limit = 16 #limit to the sum of all the player skills
        self.skill_points_limit = 10 #limit to the points of a single skill
        #skills scaling
        #game physics
        self.time_step = 1

    ##########################################################
    #----------------IMPORTING FUNCTION----------------------#
    ##########################################################

    def import_robots(self):
        #defining the robots list as empty
        self.robots = []
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
            self.number_of_robots = len(robot_list)
        #if the number of imported robots exceed the number of maximum players we raise an error
        else:
            raise ValueError('ERROR: number of robots exceeds maximum number of %s participants' %(self.player_number))
        return True

    ###############################################################
    #----------------INITIAL STATUS CREATION----------------------#
    ###############################################################

    def reset_game(self):
        '''This function is resetting the game to its initial conditions. In order to be able to start the match again.
        '''
        #removing all artists from plot
        for artist in self.ax.artists:
            print(artist)
            artist.remove()
        self.refresh_game()
        self.place_robots()
        self.draw_robots()

    def place_robots(self):
        '''This function is placing the imported robots in a specified initial position in the arena.
           This position is stored in a dictionary that will contain the current positions 
           of the robots and all their stats, in this way even if the skills change while the robot is playing 
           (trying to cheat) they will not be updated since they were copied in the initialization phase.
           The health of the robot is also given (the same for each robot) in this moment.
        '''
        counter = 0
        for robot in self.robots:
            #the self.robots_stat dictionary which holds the current status off all the participant robots 
            #is created and filled with the robots skills and positions at this moment
            self.robots_stat[robot.robot_name] = {}
            #each robot is assigned to a predefined position defined in self.initial_positions
            self.robots_stat[robot.robot_name]['position'] = self.initial_positions[counter]
            #each robot has also a color
            self.robots_stat[robot.robot_name]['color'] = self.robot_colors[counter]
            self.robots_stat[robot.robot_name]['health'] = 100
            self.robots_stat[robot.robot_name]['fired_shots'] = 0
            self.robots_stat[robot.robot_name]['suffered_hits'] = 0
            self.robots_stat[robot.robot_name]['shield'] = robot.shield
            self.robots_stat[robot.robot_name]['speed'] = robot.speed
            self.robots_stat[robot.robot_name]['power'] = robot.power
            self.robots_stat[robot.robot_name]['view_radius'] = (2 * self.robots_size) + (robot.view_radius / 10 * self.robots_size * 6)
            self.robots_stat[robot.robot_name]['shots'] = []
            self.robots_stat[robot.robot_name]['marker'] = None
            counter += 1
        
        self.robots_alive_number = counter
    
    ######################################################
    #------------MATCH EVOLUTION FUNCTION----------------#
    ######################################################

    def animate_match(self, time):
        '''This function is moving the robots according to their decisions. 
           This is done by giving them the current status in therms of other robots in the radius of view
           and positions of the shots in the range of view and asking them what is the next move 
           specified by an angular direction.
           The function also evolves the shots that were fired by the robots that are still alive. 
           If a robot is dead its shots are removed from the arena.
        '''

        #updating match time
        self.time_box.set_text('TIME: %ss' %(int(self.match_length - time)))

        #-----------NEARBY OBJECTS---------#
        #first we look for nearby robots and shots
        self.nearby_robots, self.nearby_shots = self.nearby_objects()

        #-----------QUERYING ROBOTS---------#
        #we cycle on each robot
        for robot_focus in self.robots:
            #we only ask to the robots that are still alive
            if self.robots_stat[robot_focus.robot_name]['health'] != None:

                #-------------MOVEMENT-------------#
                #then we ask the direction to the robot
                self.robots_stat[robot_focus.robot_name]['direction'] = robot_focus.move(self.robots_stat[robot_focus.robot_name]['position'], self.nearby_robots[robot_focus.robot_name], self.nearby_shots[robot_focus.robot_name])
                
                #------------SHOTS-----------------#
                #we want to shoot with a specific frequency so we check if it is the correct time to shoot
                if (time - self.shooting_time) > (1/self.shooting_freq):
                    self.shooting_time = time
                    #we ask to the robot if it wants to shoot
                    shot_dir_focus = robot_focus.shoot(self.robots_stat[robot_focus.robot_name]['position'], self.nearby_robots[robot_focus.robot_name], self.nearby_shots[robot_focus.robot_name])
                    if shot_dir_focus != None:
                        #we update the number of shots fired by the robot
                        self.robots_stat[robot_focus.robot_name]['fired_shots'] += 1
                        #we update the statistics of the robot inserting the shot information in the shots list
                        self.robots_stat[robot_focus.robot_name]['shots'].append(
                            {'position': self.robots_stat[robot_focus.robot_name]['position'], 
                            'direction': shot_dir_focus, 
                            'power': self.robots_stat[robot_focus.robot_name]['power'], 
                            'marker': None})
        
        #-----------APPLYING MOVEMENTS---------#
        #we apply the movement to both robots and shots
        for robot_focus in self.robots_stat:
            #we apply the movements only if the robot is still alive
            if self.robots_stat[robot_focus]['health'] != None:
                #moving robot
                self.robots_stat[robot_focus]['position'] = self.move_robot(robot_focus)
                #moving its shots
                self.move_shots(robot_focus)

        return True

    ##################################################
    #-------------UTILITY FUNCTIONS------------------#
    ##################################################

    def check_hit(self):
        '''This function is in charge of checking if there is a hit between each robot and 
           the shots coming from other robots. In case a hit is registered the health of the hitted 
           robot is decreased according to the power of the robot that shot the bullet and if the health 
           goes below zero the robot dies and its healt is set to None.
        '''
        #looping over the robot we want to focus on considering its nearby shots
        for robot_focus in self.nearby_shots:
            #looping over robots that shooted the nearby shots
            for robot in self.nearby_shots[robot_focus]:
                #looping over the shots
                for shot_focus in self.nearby_shots[robot_focus][robot]:
                    #we check the distance between the shots and "robot_focus"
                    if shot_focus[1] <= (self.robots_size + self.shot_size):
                        #if the robot_focus got hitted we update its statistisc
                        self.robots_stat[robot_focus]['suffered_hits'] += 1
                        #if there is a hit we reduce the "robot_focus" health according to its shield and the power of the shot
                        self.robots_stat[robot_focus]['health'] -= 10 + (shot_focus[0]['power'] + 1) - int(self.robots_stat[robot_focus]['shield']/2) 
                        #if then the health goes below or equal zero the robot dies
                        if self.robots_stat[robot_focus]['health'] <=0:
                            #we set the health to None
                            self.robots_stat[robot_focus]['health'] = None
                        #if there is a hit we also want to remove it from the arena and finally from the shots list
                        #first we delete the shot from the arena
                        self.ax.artists.remove(shot_focus[0]['marker'])
                        #then we delete the shot object itself from the robot that owns it
                        self.robots_stat[robot]['shots'].remove(shot_focus[0]) 

        #counting the number of alive robots
        count = 0
        for robot_focus in self.robots_stat:
            if self.robots_stat[robot_focus]['health'] == None:
                count += 1
        self.robots_alive_number = (self.number_of_robots - count)
        
        return True

    def move_robot(self, robot_name):
        '''This function is in charge of applying the movement to the robot, if it wants to, 
            only is this move is allowed. Moving out of the arena or through another robot is not allowed. 
            Each robot has a radius that determines its dimension and is scaled 
            according to the arena size (it is given in percentage). 
            The same happen for the velocity skill which is rescaled according to the arena size.
            
            INPUT:
            1) the name of the robot of which we want to move the position
        '''
        #scaling the velocity skill according to arena dimension
        velocity = self.robots_stat[robot_name]['speed'] /10 * self.speed_limit 

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
    
    def move_shots(self, robot_name):
        '''This function is in charge of applying the movement to the robot shots, if there are some.
            The shots are moved all with the same velocity defined in "self.speed_shot" expressed as a quantity 
            scaled to the robot maximum allowed velocity. 
            Shots have to be faster than robots otherwise the probability of getting hitted are lower 
            and the match lasts too long.
           
            INPUT:
            1) the name of the robot of which we want to move the shots 
        '''

        #first we check if the robot has shots to move
        if len(self.robots_stat[robot_name]['shots']) > 0:
            #we loop over the robot shots
            for shot_focus in self.robots_stat[robot_name]['shots']:
                #whe check if the shot went out of the arena (if yes we delete it)
                if shot_focus['position'][0] > self.arena_x_dim or shot_focus['position'][0] < 0 or shot_focus['position'][1] > self.arena_y_dim or shot_focus['position'][1] < 0:
                    #first we delete the shot from the arena
                    self.ax.artists.remove(shot_focus['marker'])
                    #then we delete the shot object itself
                    self.robots_stat[robot_name]['shots'].remove(shot_focus) 
                else:   
                    #we compute the expected final position for the focused shot
                    shift_x = self.speed_shot * np.cos(np.radians(shot_focus['direction']))
                    shift_y = self.speed_shot * np.sin(np.radians(shot_focus['direction']))
                    exp_final_pos_x = shot_focus['position'][0] + shift_x
                    exp_final_pos_y = shot_focus['position'][1] + shift_y
                    #we set the final position
                    shot_focus['position'] = (exp_final_pos_x, exp_final_pos_y)
            
        return True

    def distance(self, p1, p2):
        '''This function returns the linear distance between two points in the arena.
            INPUT:
            1) p1 = (x_1, y_1) tuple of integers
            2) p2 = (x_2, y_2) tuple of integers
            OUTPUTS:
            1) distance between the two points
        '''
        a = np.array(p1)
        b = np.array(p2)
        dist = np.linalg.norm(a-b)
        
        return dist
    
    def nearby_objects(self):
        '''This function returns the nearby objects (objects in the radius of view of each robot). 
            These are given in the form of two dictionaries.

            OUTPUT: "nearby_robots" and "nearby_shots" dictionaries structured as follows:
                    1)  nearby_robots = {
                            $robot_focus_1:{ 
                                $robot_1: {position:(x,y)
                                },
                                $robot_2:{position:(x,y)
                                },
                                ...
                            },
                            $robot_focus_2:{ 
                                $robot_1: {position:(x,y)
                                },
                                $robot_2:{position:(x,y)
                                },
                                ...
                            },
                            ...
                        }
                    2)  nearby_shots = {
                            $robot_focus_1:{ 
                                $robot_1: [[{position: (x_1_1,y_1_1), direction: dir_1_1, power:pow_1_1}, distance_1_1],
                                            [{position: (x_1_2,y_1_2), direction: dir_1_1, power:pow_1_2}, distance_1_2],
                                            ...
                                            [{position: (x_1_n,y_1_n), direction: dir_1_n, power:pow_1_n}, distance_1_n]
                                ],
                                $robot__2: [[{position: (x_2_1,y_2_1), direction: dir_2_1, power:pow_2_1}, distance_2_1],
                                            [{position: (x_2_2,y_2_2), direction: dir_2_1, power:pow_2_2}, distance_2_2],
                                            ...
                                            [{position: (x_2_n,y_2_n), direction: dir_1_n, power:pow_2_n}, distance_2_n]
                                ],
                                ...
                            }
                            $robot_focus_m:{
                                $robot_1: [[{position: (x_1_1,y_1_1), direction: dir_1_1, power:pow_1_1}, distance_1_1],
                                            [{position: (x_1_2,y_1_2), direction: dir_1_1, power:pow_1_2}, distance_1_2],
                                            ...
                                            [{position: (x_1_n,y_1_n), direction: dir_1_n, power:pow_1_n}, distance_1_n]
                                ],
                                $robot__2: [[{position: (x_2_1,y_2_1), direction: dir_2_1, power:pow_2_1}, distance_2_1],
                                            [{position: (x_2_2,y_2_2), direction: dir_2_1, power:pow_2_2}, distance_2_2],
                                            ...
                                            [{position: (x_2_n,y_2_n), direction: dir_1_n, power:pow_2_n}, distance_2_n]
                                ],
                                ...
                            }
                        }
        '''

        #everytime this function is called the two dictionaries for 
        #nearby robots and nearby shots are initialized
        nearby_robots = {}
        nearby_shots = {}
        
        #we loop over the focused robots
        for robot_focus in self.robots_stat:
            
            #we consider only the alive robots
            if self.robots_stat[robot_focus]['health'] != None:
                
                #first we have to create the dictionary for the correspondent robot that we are focusing on
                nearby_robots[robot_focus] = {}
                nearby_shots[robot_focus] = {}
                
                #we loop over the robots
                for robot in self.robots_stat:
                    #ignoring the focused robot or the dead robots
                    if robot != robot_focus and self.robots_stat[robot]['health'] != None:
                        
                        #-------------ROBOTS------------------#
                        #selecting robots in radius of view
                        curr_distance = self.distance(self.robots_stat[robot_focus]['position'], self.robots_stat[robot]['position'])
                        if curr_distance <= self.robots_stat[robot_focus]['view_radius']:
                            nearby_robots[robot_focus][robot] = {'position': self.robots_stat[robot]['position'], 'distance': curr_distance}
                        
                        #-------------SHOTS------------------#
                        #selecting shots in radius of view
                        if len(self.robots_stat[robot]['shots']) > 0:
                            #scanning through all the fired shots
                            for shot_focus in self.robots_stat[robot]['shots']:
                                #checking if the focused shot is inside the radius ov view of the focused robot
                                curr_distance = self.distance(self.robots_stat[robot_focus]['position'], shot_focus['position'])
                                if curr_distance <= self.robots_stat[robot_focus]['view_radius']:
                                    #if this is the first nearby shot that is found we have to initialize the list
                                    if robot not in nearby_shots[robot_focus]:
                                        nearby_shots[robot_focus][robot] = []
                                    #appending the nearby shot to the existing list
                                    nearby_shots[robot_focus][robot].append([shot_focus, curr_distance])
            
        return nearby_robots, nearby_shots

    ####################################################
    #--------------GRAPHICAL FUNCTIONS-----------------#
    ####################################################
    
    def generate_arena(self): 
        #reading the image that has to be used as arena background
        img = plt.imread("img/robot_wars_arena.jpg")
        #generating the arena figure and axes
        self.fig = plt.figure(figsize=(9,7))
        self.ax = self.fig.add_subplot(111)
        #placing the arena image as background
        self.ax.imshow(img, zorder=0, extent=[1.0, self.arena_x_dim, 1.0, self.arena_y_dim])
        #placing the time on the top of the arena
        self.time_box = self.ax.text(35, 105, 'TIME: %ss' %(self.match_length), fontsize=20)
        self.create_game_window()
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
            self.refresh_game()
            time.sleep(1)
        #at the end of the countdown after the message has been displayed we remove it and the match starts
        countdown_obj.remove()
        self.refresh_game()
        
    def draw_robots(self):
        #placing the robots in the arena
        for robot in self.robots_stat:
            if self.robots_stat[robot]['marker'] in self.ax.artists:
                #self.ax.artists.remove(self.robots_stat[robot]['marker'])
                self.robots_stat[robot]['marker'].center = (self.robots_stat[robot]['position'])
                if self.robots_stat[robot]['health'] == None:
                    self.robots_stat[robot]['marker'].set_facecolor('lightgray')
            else:
                self.robots_stat[robot]['marker'] = plt.Circle(self.robots_stat[robot]['position'], self.robots_size, color=self.robots_stat[robot]['color'])
                if self.robots_stat[robot]['health'] == None:
                    self.robots_stat[robot]['marker'].set_facecolor('lightgray')
                self.ax.add_artist(self.robots_stat[robot]['marker'])

        self.refresh_game()
        return True
    
    def draw_shots(self):
        #placing the shots in the arena
        for robot in self.robots_stat:
            for shot_focus in self.robots_stat[robot]['shots']:
                if shot_focus['marker'] in self.ax.artists:
                    shot_focus['marker'].center = (shot_focus['position'])
                else:
                    shot_focus['marker'] = plt.Circle(shot_focus['position'], self.shot_size, color=self.robots_stat[robot]['color'])
                    self.ax.add_artist(shot_focus['marker'])
         
        self.refresh_game()
        return True
    
    def create_game_window(self):
        self.start = False
        self.pause = False
        self.reset = False
        self.root = tk.Tk()

        #-----------frame left--------------------
        self.frame_image = tk.Frame(self.root, highlightbackground="black", highlightthickness=1, relief='raised')
        self.frame_image.grid(row=0, column=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_image)
        plot_widget = self.canvas.get_tk_widget()
        plot_widget.pack(side='top')

        #----------frame right--------------------
        self.frame_right = tk.Frame(self.root)
        self.frame_right.grid(row=0, column=1)
        
        #-----------frame buttons-----------------
        self.frame_buttons = tk.Frame(self.frame_right)
        self.frame_buttons.grid(row=0, column=0)
        Button_Start = tk.Button(self.frame_buttons,text="Start", command=self.start_trigger)
        Button_Start.pack(side='left', padx = 10)
        Button_Pause = tk.Button(self.frame_buttons,text="Pause", command=self.pause_trigger)
        Button_Pause.pack(side='left', padx = 10)
        Button_Reset = tk.Button(self.frame_buttons,text="Reset", command=self.reset_trigger)
        Button_Reset.pack(side='left', padx = 10)
        Button_Quit = tk.Button(self.frame_buttons,text="Quit", command=self.quit)
        Button_Quit.pack(side='left', padx = 10)

        #-----------frame players stats------------
        self.frame_stats = tk.Frame(self.frame_right, highlightbackground="black", highlightthickness=1)
        self.frame_stats.grid(row=1, column=0)
        #titleframe
        self.frame_stats_title = tk.Frame(self.frame_stats)
        self.frame_stats_title.grid(row=0, column=0)
        titleLabel = tk.Label(self.frame_stats_title, font=('arial', 16, 'bold'),
                        text="Robots statistics",
                        bd=5)
        titleLabel.pack(side='top')
        #statistics_frame
        self.frame_stats_numbers = tk.Frame(self.frame_stats)
        self.frame_stats_numbers.grid(row=1, column=0)
        # headers of the columns
        header_name = tk.Label(self.frame_stats_numbers, font=('arial', 14, 'bold'),
                            text="Name", bd=5).grid(row=0, column=0)
        header_health = tk.Label(self.frame_stats_numbers, font=('arial', 14, 'bold'),
                            text="Health", bd=5).grid(row=0, column=1)
        header_fired = tk.Label(self.frame_stats_numbers, font=('arial', 14, 'bold'),
                            text="Fired shots", bd=5).grid(row=0, column=2)
        header_suffered = tk.Label(self.frame_stats_numbers, font=('arial', 14, 'bold'),
                            text="Suffered hits", bd=5).grid(row=0, column=3)

        #this is the dictionary that will contain the labels for the players statistics
        self.robots_stat_labels = {}
        count = 1
        for robot_focus in self.robots_stat:
            self.robots_stat_labels[robot_focus] = {}
            self.robots_stat_labels[robot_focus]['name'] = tk.Label(self.frame_stats_numbers, font=('arial', 12, 'bold'),
                                                        text="%s" %(robot_focus), bd=5, foreground=self.robots_stat[robot_focus]['color'])
            self.robots_stat_labels[robot_focus]['name'].grid(row=count, column=0)
            self.robots_stat_labels[robot_focus]['health'] = tk.Label(self.frame_stats_numbers, font=('arial', 12, 'bold'),
                                                        text="%s" %(self.robots_stat[robot_focus]['health']),
                                                        bd=5, foreground=self.robots_stat[robot_focus]['color'])
            self.robots_stat_labels[robot_focus]['health'].grid(row=count, column=1)
            self.robots_stat_labels[robot_focus]['fired'] = tk.Label(self.frame_stats_numbers, font=('arial', 12, 'bold'),
                                                        text="%s" %(self.robots_stat[robot_focus]['fired_shots']),
                                                        bd=5, foreground=self.robots_stat[robot_focus]['color'])
            self.robots_stat_labels[robot_focus]['fired'].grid(row=count, column=2)
            self.robots_stat_labels[robot_focus]['suffered'] = tk.Label(self.frame_stats_numbers, font=('arial', 12, 'bold'),
                                                        text="%s" %(self.robots_stat[robot_focus]['suffered_hits']),
                                                        bd=5, foreground=self.robots_stat[robot_focus]['color'])
            self.robots_stat_labels[robot_focus]['suffered'].grid(row=count, column=3)

            count += 1
    
    def refresh_stat_labels(self):
        '''This function has the purpose of refreshing the statistics of the robots 
            that are displayed in the game interface
        '''
        for robot_focus in self.robots_stat_labels:
            self.robots_stat_labels[robot_focus]['health'].config(text="%s" %(self.robots_stat[robot_focus]['health']))
            self.robots_stat_labels[robot_focus]['fired'].config(text="%s" %(self.robots_stat[robot_focus]['fired_shots']))
            self.robots_stat_labels[robot_focus]['suffered'].config(text="%s" %(self.robots_stat[robot_focus]['suffered_hits']))
    
    def refresh_game(self):
        self.canvas.draw()
        self.refresh_stat_labels()
        self.root.update()
    
    def quit(self):
        self.root.destroy()
    
    def start_trigger(self):
        self.start = True
        self.reset = False
        self.pause = False
    
    def pause_trigger(self):
        self.pause = True
        self.start = False
        self.reset = False
    
    def reset_trigger(self):
        self.reset = True
        self.pause = True
        self.start = False

