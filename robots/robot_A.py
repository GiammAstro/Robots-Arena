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
            A higher total number of skill points is not accepted.
        '''
        self.speed = 0
        self.power = 4
        self.view_radius = 8
        self.shield = 4
        return True
    
    def move(self, pos, players_in_radius, shots_in_radius):
        '''Here you can chose how you want your robot to move in the arena,
            basing on the information that you have consisting in:
            1) position of the robot "pos" as a tuple (x,y)
            2) position of the other robots in the view radius as tuple (x,y) 
               accessible by "pos" property of "robots_in_radius" list objects
            3) position of the shots in the view radius as tuple (x,y) 
               accessible by "pos" property of "shots_in_radius" list objects
            
            OUTPUT: Basing on the information you have and on the speed that you selected 
            you have to consider how you want to move your robot. You can implement your own logic 
            for chosing how your robot should behave but the output has to be given chosing 
            the movement direction among the 9 different possibilities:
            1) "UP": for moving up 
            2) "DN": for moving down
            3) "LX": for moving left
            4) "RX": for moving right
            5) "UL": for moving up-left
            6) "UR": for moving up-right
            7) "DL": for moving down-left
            8) "DR": for mobing down-right
            9) None of the previous for standing still
        '''
        direction = ''
        return direction