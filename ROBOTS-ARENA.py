from game_app import game
import time

#instantiating the game class
game = game()

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
    while time.time() - start_time < game.match_length:
        #starting evolving the match
        game.animate_match()
        game.draw_robots()
        time.sleep(0.1)
    
    
    

main()