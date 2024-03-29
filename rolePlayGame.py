###########################################  PYTHON TEXT BASED ROLE PLAY GAME  ############################################
# Importing all the required libraries
import random
import os
import time
import sys
import textwrap
import cmd

screen_width = 100

####### Player Setup #######
class player:
    def __init__(self):                 # __init__() is a method in python
        self.name = ""
        self.job = ""
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'b2'
        self.game_over = False
my_player = player()      

##################  Title Screen  ###################
def title_screen():
    os.system('clear')
    print("########################################")
    print("#  Welcome to the Text Role Play Game  #")
    print("########################################")
    print("              - Play -                   ")
    print("              - Help -                   ")
    print("              - Quit -                   ")
    title_screen_selections()

def title_screen_selections():
    option = input("> ")
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        print("***** THANK YOU FOR VISITING *****")
        sys.exit()
    while option not in ['play', 'quit', 'help']:
        print("You have typed something INVALID. Type again-")  
        option = input("> ")
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        print("***** THANK YOU FOR VISITING *****")
        sys.exit()  

def help_menu():
    print(" ########################################")
    print(" # Welcome to the Help Menu of Text RPG #")
    print(" ########################################")
    print(" - Use up, down, left, right to move ")
    print(" - Type your commands (play, help or quit) to do them")
    print(' - Use "look" to inspect  something')
    print(" !!!!!!! Good luck and have fun !!!!!!!")
    title_screen_selections()

####################  MAP  #######################
"""                               
______________________________

|   a1  |  a2  |  a3  |  a4   |   ### Player Starts at b2 ### 
______________________________
                                  ******* This is the visualization of our map (4 x 4) *******
|  b1   |  b2  |  b3  |  b4  |
______________________________   
                                 
|  c1   |  c2  |  c3  |  c4  |
______________________________

|  d1   |  d2  |  d3  |  d4  |
______________________________      """

ZONEMAP = 'TOWN'
DESCRIPTION = 'You are wandering in a town.'
EXAMINATION = 'Have fun!!!'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

solved_places = { 'a1' : False, 'a2' : False, 'a3' : False, 'a4' : False,
                  'b1' : False, 'b2' : False, 'b3' : False, 'b4' : False,
                  'c1' : False, 'c2' : False, 'c3' : False, 'c4' : False,
                  'd1' : False, 'd2' : False, 'd3' : False, 'd4' : False,
}

zonemap = {
    'a1' : {
        ZONEMAP : 'Town Market',
        DESCRIPTION : 'You can shop whatever you want.',
        EXAMINATION : 'Thi market is very famous in the town.',
        SOLVED : False,
        UP : 'OUT_OF_TOWN',
        DOWN : 'b1',
        LEFT : 'OUT_OF_TOWN',
        RIGHT : 'a2'
    },
    'a2' : {
        ZONEMAP : 'Town Entrance',
        DESCRIPTION : 'Entrance to the main town',
        EXAMINATION : 'You are now entering the town',
        SOLVED : False,
        UP : 'OUT_OF_TOWN',
        DOWN : 'b2',
        LEFT : 'a1',
        RIGHT : 'a3'
    },
    'a3' : {
        ZONEMAP : 'Town Square',
        DESCRIPTION : 'Public square for community gathering.',
        EXAMINATION : 'A public gathering is going on. You too can participate.',
        SOLVED : False,
        UP : 'OUT_OF_TOWN',
        DOWN : 'b3',
        LEFT : 'a2',
        RIGHT : 'a4'
    },
    'a4' : {
        ZONEMAP : 'Town Hall',
        DESCRIPTION : 'Hall for the discussions',
        EXAMINATION : 'Participate in the discussion. You may get free Pizzas.',
        SOLVED : False,
        UP : 'OUT_OF_TOWN',
        DOWN : 'b4',
        LEFT : 'a3',
        RIGHT : 'OUT_OF_TOWN'
    },
    'b1' : {
        ZONEMAP : 'Church',
        DESCRIPTION : 'You can pray to the JESUS.',
        EXAMINATION : 'Pray.',
        SOLVED : False,
        UP : 'a2',
        DOWN : 'c1',
        LEFT : 'OUT_OF_TOWN',
        RIGHT : 'b2'
    },
    'b2' : {
        ZONEMAP : 'Home',
        DESCRIPTION : 'This is your home!',
        EXAMINATION : 'Your home looks the same - nothing has changed.',
        SOLVED : False,
        UP : 'a2',
        DOWN : 'c2',
        LEFT : 'b1',
        RIGHT : 'b3'
    },
    'b3' : {
        ZONEMAP : 'School',
        DESCRIPTION : 'Best school in the entire town.',
        EXAMINATION : 'You can go to school and meet your friends.',
        SOLVED : False,
        UP : 'a3',
        DOWN : 'c3',
        LEFT : 'b2',
        RIGHT : 'b4'
    },
    'b4' : {
        ZONEMAP : 'Hospital',
        DESCRIPTION : 'Doctors are great in this hospital.',
        EXAMINATION : 'If you are hurt, you can be treated here.',
        SOLVED : False,
        UP : 'a4',
        DOWN : 'c4',
        LEFT : 'b3',
        RIGHT : 'OUT_OF_TOWN'
    },
    'c1' : {
        ZONEMAP : 'Medical Store',
        DESCRIPTION : 'Medical store nearest to the hospital.',
        EXAMINATION : 'Collect all the medicines you require for yourself.',
        SOLVED : False,
        UP : 'b1',
        DOWN : 'd1',
        LEFT : 'OUT_OF_TOWN',
        RIGHT : 'c2'
    },
    'c2' : {
        ZONEMAP : 'Play Ground',
        DESCRIPTION : 'You can Play Basketball, Badminton, Hockey, Football, Cricket here.',
        EXAMINATION : 'Play with your friends.',
        SOLVED : False,
        UP : 'b2',
        DOWN : 'd2',
        LEFT : 'c1',
        RIGHT : 'c3'
    },
    'c3' : {
        ZONEMAP : 'Garden',
        DESCRIPTION : 'Children play here in swings.',
        EXAMINATION : 'Have fun with your friends.',
        SOLVED : False,
        UP : 'b3',
        DOWN : 'd3',
        LEFT : 'c2',
        RIGHT : 'c4'
    },
    'c4' : {
        ZONEMAP : 'Government Office',
        DESCRIPTION : 'All the government procedings are organized here.',
        EXAMINATION : 'None of our business. We are here to have fun.',
        SOLVED : False,
        UP : 'b4',
        DOWN : 'd4',
        LEFT : 'c3',
        RIGHT : 'OUT_OF_TOWN'
    },
    'd1' : {
        ZONEMAP : 'City Mall',
        DESCRIPTION : 'Mall is a great place.',
        EXAMINATION : 'Enjoy here.',
        SOLVED : False,
        UP : 'c1',
        DOWN : 'OUT_OF_TOWN',
        LEFT : 'OUT_OF_TOWN',
        RIGHT : 'd2'
    },
    'd2' : {
        ZONEMAP : 'Movie Hall',
        DESCRIPTION : 'You can watch movie with your friends and family.',
        EXAMINATION : 'Watch End Game.',
        SOLVED : False,
        UP : 'c2',
        DOWN : 'OUT_OF_TOWN',
        LEFT : 'd1',
        RIGHT : 'd3'
    },
    'd3' : {
        ZONEMAP : 'Restaurant',
        DESCRIPTION : 'You will be served delicious food and snacks here.',
        EXAMINATION : 'Food is life - and you seem to be hungry.',
        SOLVED : False,
        UP : 'c3',
        DOWN : 'OUT_OF_TOWN',
        LEFT : 'd2',
        RIGHT : 'd4'
    },
    'd4' : {
        ZONEMAP : 'Metro Station',
        DESCRIPTION : 'You can board a metro from here.',
        EXAMINATION : 'Come-on lets go back home.',
        SOLVED : False,
        UP : 'c4',
        DOWN : 'OUT_OF_TOWN',
        LEFT : 'd3',
        RIGHT : 'OUT_OF_TOWN'
    },
    'OUT_OF_TOWN' : {
        ZONEMAP : 'OUT_OF_TOWN',
        DESCRIPTION : 'You are out of the town.',
        EXAMINATION : 'You will now be sent back to Home.',
        SOLVED : False,
        UP : 'b2',
        DOWN : 'b2',
        LEFT : 'b2',
        RIGHT : 'b2'
    }
} 

##########  Game Interactivity  ##########
def print_location():
    print("\n****************************************************************")
    print("Your Location : " + my_player.location.upper())
    print("Zonemap :" + zonemap[my_player.location][ZONEMAP])
    print("Description :" + zonemap[my_player.location][DESCRIPTION])
    print("Examination :" + zonemap[my_player.location][EXAMINATION])
    print("****************************************************************\n")
    zonemap[my_player.location][SOLVED] = True

def prompt():
    print("\n" + "========================================================")
    print("What would you like to do now?\nYou can- move, go, travel, walk, quit, examine, inspect, interact or look.")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look']

    while action.lower() not in  acceptable_actions:
        print("Unknown action, try again")
        action = input("> ")
    if action.lower() == 'quit':
        print("***** Thank you for visiting *****")
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        player_examine()

def player_move(myAction):
    ask = "Where would you like to " + myAction.lower() + "?\n"
    print("You can go- up/north, down/south, right/east, left/west.")
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[my_player.location][UP]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[my_player.location][LEFT]
        movement_handler(destination) 
    elif dest in ['right', 'east']:
        destination = zonemap[my_player.location][RIGHT]
        movement_handler(destination) 
    elif dest in ['down', 'south']:
        destination = zonemap[my_player.location][DOWN]
        movement_handler(destination)  
    while dest.lower() not in ['up', 'north', 'down', 'south', 'right', 'east', 'left', 'west']:
        print("You have entered something INVALID. Please type something valid.")
        ask = "Where would you like to " + myAction.lower() + "?\n"
        print("You can go- up/north, down/south, right/east, left/west.")
        dest = input(ask)
        if dest in ['up', 'north']:
            destination = zonemap[my_player.location][UP]
            movement_handler(destination)
        elif dest in ['left', 'west']:
            destination = zonemap[my_player.location][LEFT]
            movement_handler(destination) 
        elif dest in ['right', 'east']:
            destination = zonemap[my_player.location][RIGHT]
            movement_handler(destination) 
        elif dest in ['down', 'south']:
            destination = zonemap[my_player.location][DOWN]
            movement_handler(destination)
           

def movement_handler(destination):
    print("\n" + "You have moved to the " + destination.upper() + ".")
    my_player.location = destination
    print_location()

def player_examine():
    if zonemap[my_player.location][SOLVED]:
        print("You have already exhausted this zone.")
    else :
        print("You can trigger a puzzle here.")    

########### Game Functionality ############
def main_game_loop():
    while my_player.game_over is False:
        prompt()
        # If puzzle has been solved, boss defeated, explored everything etc.

def setup_game():
    #os.system('clear')

    ######### Name Collecting ###########
    question1 = "Hello, what's your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")    
    my_player.name = player_name 

    question2 = "Hello my friend " + my_player.name + ", what role do you want to play?\n"
    question2added = "You can play as a warrior, priest or mage.\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)    
    player_job = input("> ")  
    valid_jobs = ['warrior', 'mage', 'priest']  
    if player_job.lower() in valid_jobs:
        my_player.job = player_job
        print("Great! You are now a " + my_player.job + "!!!")
    while player_job.lower() not in valid_jobs:
        player_job = input("> ")
        if player_job.lower() in valid_jobs:
            my_player.job = player_job

    ################ Player Stats ###############
    if my_player.job is 'warrior':
        self.hp = 120
        self.mp = 20
    if my_player.job is 'mage':
        self.hp = 40
        self.mp = 120
    if my_player.job is 'priest':
        self.hp = 60
        self.mp = 60

    ########### Introduction #############
    question3 = player_name.upper() + ", the " + player_job + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    speech1 = "Welcome to this fantasy world!!!!!!!\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    speech2 = "I hope it greets you well.\n"
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    speech3 = "Just make sure you don't get too lost.\n"
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    speech4 = "Hehehehehe...\n"
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)

    ##os.system('clear')  
    print("#######################################")  
    print("##        Let's start now !!!        ##")
    print("#######################################")
    main_game_loop()

title_screen()
###############################################  END OF PROGRAM  ###################################################