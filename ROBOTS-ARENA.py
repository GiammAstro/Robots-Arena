#from gui import game_gui
from game_app import game
import time
import sys

#graphical settings
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

    #--------MATCH EVOLUTION-------------
    delta_time = 0 #the time since the match started is set to zero
    countdown = True # when we will press on start we want the countdown to be shown
    
    #we loop until the maximum time is not finished or there is a winner
    while delta_time < match_length + 1 and game.robots_alive_number != 1:
        
        #for every loop we refresh the game 
        #(this refreshes the current value of the triggers and allows us 
        #to understand if a button has been pressed)
        game.refresh_game()

        #------ON QUIT PRESS--------
        if game.quit == True:
            break
        
        #------ON PAUSE PRESS--------
        if game.pause == True:
            while (game.start != True) and (game.reset != True):
                time.sleep(0.1)
                game.refresh_game()
        
        #-----ON RESET PRESS---------
        if game.reset == True:
            delta_time = 0
            countdown = True
            #resetting the match
            game.reset_game()
            game.reset = False
        
        #----ON START PRESS----------
        if game.start == True:
            if countdown == True:
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
    
    if game.robots_alive_number == 1:
        game.show_winner()
        time.sleep(10)
    else:
        game.show_no_winner()
        time.sleep(10)

if __name__ == '__main__':              
    main()