class robot():
    
    def __init__(self):
        self.robot_name = 'ROBOT_A'
        self.skills()

    def skills(self):
        '''In this function you can thefine the 4 skills of your robot which are:
            1) the speed "self.speed"
            2) the shooting power "self.power"
            3) the view radius "self.view_radius"
            4) the shield of the robot "self.shield"
            
            REMEMBER: you have a maximum of 16 robot skill points to give to your robot. 
            A higher total number of skill points is not accepted. Each skill can have a maximum of 10 points
            so as example a speed of 11 or 16 is not allowed.
        '''
        self.speed = 1
        self.power = 4
        self.view_radius = 0
        self.shield = 0
        return True
    
    def move(self, position, players_in_radius, shots_in_radius):
        '''Here you can chose how you want your robot to move in the arena,
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
        self.direction = 45
        return self.direction
    
    def shoot(self, position, players_in_radius, hots_in_radius):
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
        self.shot = self.direction
        return self.shot