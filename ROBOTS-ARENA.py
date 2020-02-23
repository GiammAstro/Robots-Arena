from game_app import game
import time
import sys

#Game graphical settings
fps = 60
match_length = 120

#instantiating the game class
game = game(fps)

#----------------MAIN---------------------
def main():

    #--------MATCH INITIALIZATION---------
    #importing the robots in the robots folder
    game.import_robots()
    #placing the robots in their initial position
    game.place_robots()
    #generating the arena
    game.generate_arena()
    #drawing the robots in the arena on their initial position
    game.draw_robots()

    #--------MATCH COUNTDOWN-------------
    #countdown
    game.display_countdown()
    
    #--------MATCH EVOLUTION-------------
    start_time = time.time()
    while time.time() - start_time < match_length + 1:
        #starting evolving the match
        game.animate_match(time.time() - start_time)
        game.draw_robots()
        game.draw_shots()
        time.sleep(1/fps)
        sys.stdout.flush()
    
    
main()