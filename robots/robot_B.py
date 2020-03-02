class robot():
    
    def __init__(self):
        self.robot_name = 'ROBOT_temp'
        self.skills()

    def skills(self):
        '''In this function you can define the 4 skills of your robot which are:
            1) the speed "self.speed"
            2) the shooting power "self.power"
            3) the view radius "self.view_radius"
            4) the shield of the robot "self.shield"
            
            REMEMBER: you have a maximum of 16 robot skill points to give to your robot. 
            A higher total number of skill points is not accepted.
        '''
        self.speed = 0
        self.power = 0
        self.view_radius = 0
        self.shield = 0
        return True
    
    def move(self, __pos, __players_in_radius, __shots_in_radius):
        '''Here you can chose how you want your robot to move in the arena,
            basing on the information that you have consisting in:
            1) position of the robot "pos" as a tuple (x,y)
            2) position of the other robots in the view radius as tuple (x,y) 
               accessible by "pos" property of "robots_in_radius" dictionary objects
            3) position of the shots in the view radius as tuple (x,y) 
               accessible by "pos" property of "shots_in_radius" dictionary objects
            
            OUTPUT: Basing on the information you have and on the speed that you selected 
            you have to consider how you want to move your robot. You can implement your own logic 
            for chosing how your robot should behave but the output has to be given chosing 
            the movement direction expressed in the form of the angular direction in the field 
            (clockwise from the vertical up direction) given in degrees. If no direction is given ("direction" = None) the robot will stand still
        '''
        direction = None
        return direction
    
    def shoot(self, __pos, __players_in_radius, __shots_in_radius):
        ''''Here you can chose how you want your robot to shoot in the arena,
            basing on the information that you have consisting in:
            1) position of the robot "pos" as a tuple (x,y)
            2) position of the other robots in the view radius as tuple (x,y) 
               accessible by "pos" property of "robots_in_radius" dictionary objects
            3) position of the shots in the view radius as tuple (x,y) 
               accessible by "pos" property of "shots_in_radius" dictionary objects
            
            OUTPUT: Basing on the information you have and on the speed that you selected 
            you have to consider how you want to move your robot to shoot. You can implement your own logic 
            for chosing how your robot should behave but the output has to be given  in the form of:
            1) the direction of the shots expressed in the form of the angular direction in the field 
               (clockwise from the orizontal right direction, corresponding to the positive x axis) given in degrees. 
               If no direction is given ("shot" = None) the robot will not shoot
        '''
        self.shot = None
        return self.shot