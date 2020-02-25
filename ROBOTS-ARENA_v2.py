#from gui import game_gui
from game_app import game
import time
import sys

#Game graphical settings
fps = 60
match_length = 120

#instantiating the game class
game = game(fps, match_length)

#----------------MAIN---------------------
def main():

    #--------GAME INITIALIZATION---------
    #importing the robots in the robots folder
    game.import_robots()
    #creating the robots and assigning them their initial position
    game.place_robots()
    #generating the arena
    game.generate_arena()
    #drawing the robots in the arena
    game.draw_robots()

    #-------USER START INPUT-------------
    #while game.start == False:
    #    game.refresh_game()

    #--------MATCH COUNTDOWN-------------
    #countdown
    #game.display_countdown()
    
    #--------MATCH EVOLUTION-------------
    delta_time = 0
    countdown = True
    #we loop until the maximum time is not finished or there is a winner
    while delta_time < match_length + 1 or game.robots_alive_number != 1:
        
        #for every loop we refresh the game
        game.refresh_game()
        
        if game.pause == True:
            while (game.start != True) and (game.reset != True):
                time.sleep(0.1)
                game.refresh_game()
        
        if game.reset == True:
            delta_time = 0
            countdown = True
            #--------MATCH RESET---------
            #resetting the match
            game.reset_game()
            game.reset = False
            
        #-------USER START INPUT-------------
        #while game.start == False:
        #    game.refresh_game()

        if game.start == True:
            if countdown == True:
                #--------MATCH COUNTDOWN-------------
                #countdown
                game.display_countdown()
                countdown = False

            #--------MATCH EVOLUTION-------------
            #starting evolving the match
            time_1 = time.time()
            game.animate_match(delta_time)
            game.check_hit()
            game.draw_robots()
            game.draw_shots()
            time.sleep(1/fps)
            sys.stdout.flush()
            delta_time += time.time() - time_1
              
main()