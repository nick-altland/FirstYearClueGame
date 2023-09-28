#Nicholas Altland
#CLUE: The Game
#This is the game of clue, a murder mystery where you, the user, will try and discover who is the killer
#and who is innocent. 

#Import modules
import random
import math

#declare constants
ASK_QUESTION = 1
SEE_NOTEPAD = 2
FINAL_GUESS = 3
MENU_LENGTH = 3

#input validation
#This function looks at the input from a user and validates that it meets the parameters set 
#Paramters are: string for user input, whether the answer is alpha or numeric, and how many options to choose from
def input_validation(string, input_type, option_range):
    
    #Sets the variable valid to false
    valid = False
    
    #If the input type is supposed to be an alpha character, go through this loop
    if input_type == "alpha":
        #turn the option_range into a string
        option_range_string = ', '.join(option_range).title()
        #The answer user input, using the string provided
        answer = input(f"{string} {option_range_string}:   ").title()
        
        #While the answer is not a valid option
        while valid != True:
            #For every item in the list
            for item in option_range:
                #If answer not in the list, make sure that it is
                if answer not in option_range:
                    print(f'"{answer}" is not an option, make sure to pick an option from: {option_range_string}')
                    answer = input(f"{string} {option_range_string}:   ").title()
                #if the answer is valid, set valid = to True
                else:
                    valid = True
                    
    #If the input type is supposed to be a numeric character, go through this loop
    if input_type == "numeric":
        #The answer the user inputs, using the string provided
        answer = input(f"{string}")
        
        #While valid is not True
        while valid != True:
            #If the user input is not a numeric value, tell them to enter a numeric value
            if answer.isnumeric() != True: 
                print(f"{answer} is not an option. Be sure to enter a numeric character")
                answer = input(f"{string}")
            
            #If the answer is a numeric value, turn the answer into an int
            elif answer.isnumeric() == True:
                answer = int(answer)
                #If the answer is not in the range provided, tell user that it is not in the range
                if answer not in range(1, option_range+1):
                    print(f"{answer} is not on option, be sure that it is not too high/low")
                    answer = input(f"{string}")
                #If the answer is valid, set answer to valid
                else:
                    valid = True
    
    #If there is a mistake in parameters, this tells me to fix it
    #Purely for debugging purposes
    if input_type != "alpha" and input_type != "numeric":
        answer = "Be sure to set an input type to either 'alpha' or 'numberic'."
    
    '''Templates for function input:
        
        input_validation("answer 1, 2, or 3:   ", "numeric", 3)
        input_validation("answer y or n:   ", "alpha", ["y", "n"])
        
    End Template for input Validation'''
    
    #Return the answer after it has been validated
    return answer


def tutorial():
    
    suspects = ("Miss Scarlet", "Colonel Mustard", "Mrs. White")
    weapons = ("Wrench", "Candlestick", "Lead Pipe")
    rooms = ("Kitchen", "Ball Room", "Conservatory", "Dinning Room")
    
    
    #Print short message outlining the game
    print(), print("Clue is a game about discovering what the other players know. However, before that, you must pick your character! Let’s give it a shot! A list of characters will appear below. Follow the instructions to select who you want to play as.")
    print()
    
    non_player_characters = []#Empty list for non_player_characters to go to
    
    #Let's the user pick their character, and asigns the remaining to the NPC list
    player_character, non_player_characters = pick_character(suspects, non_player_characters)

    #asigns the murder items
    murder_details = ["Miss Scarlet", "Wrench", "Kitchen"]
    
    #Flavor text to let the player know that the items have been delt
    print(), print("The deck of items is shuffled and delt to the players at the table.")
    
    #Asign player and non player hands
    player_hand = ["Colonel Mustard", "Lead Pipe", "Ball Room"]
    non_player_hands = {non_player_characters[0]: ["Mrs. White", "Candlestick"], non_player_characters[1]: ["Conservatory", "Dinning Room"]}
    
    #Tell the player what items they have in their hand
    print(f"You have the following items: {', '.join(player_hand)}"), print()
    
    #Call tup to dic to set up notepad for later on
    suspects_dict, weapons_dict, rooms_dict = tup_to_dict(suspects, weapons, rooms)
    
    #Introduce the notepad, tell them what it means.
    print(), print("Okay, now that you have decided who to play as and gotten your cards, let's look at what we have so far"), print()
    input_validation("To look at your notepad, press ", "alpha", "2")
    #Call and print the notepad
    notepad(player_hand, suspects_dict, weapons_dict, rooms_dict)
    print(), print("This is your notepad! It shows all the suspects, weapons, and rooms in the game")
    print("You see those little 'X'? That means you have discovered those items, and they CANNOT be the murderer, murder weapon, or murder location")
    print("Let's try to uncover a little more information to fill out your notepad")
    print(), input_validation("Let's ask a question to uncover more information. Start with a suspect, someone you think is guilty. Then a weapon. Then a room. To ask a question, press", "alpha", "1")
    
    #Call the function question answer to have them ask a question
    new_information = question_answer(player_hand, non_player_hands, suspects, weapons, rooms)
    #update the player's hand with the new information
    player_hand.append(new_information)
    print(), print("Okay, so let's pretend that this goes on a few rounds and you have uncovered all the information everyone else at the table knows")
    
    player_hand = ["Colonel Mustard", "Lead Pipe", "Ball Room", "Mrs. White", "Candlestick", "Conservatory", "Dinning Room"] 
    input_validation("Let's check your notepad to see what you have learned. Remember, press ", "alpha", "2")
    notepad(player_hand, suspects_dict, weapons_dict, rooms_dict)
    print(), print("Wow! Look at that! There are three details missing, one from each catagory. Hmmm, this must mean they were the Murderer, Murder weapon, and the Murder location!!!!")
    print("Okay! It is time to make our final guess!")
    input_validation("Tp make your final accusation, press ", "alpha", "3")
    input_validation("Who is the murderer?: hint, its", "alpha", ["Miss Scarlet"])
    input_validation("What is the murder weapon?: hint, its the", "alpha", ["Wrench"])
    input_validation("Where is the murder location?: hint, its the", "alpha", ["Ball Room"])
    print(), print(f"That is correct!!! The murderer is {murder_details[0]}, with the {murder_details[1]}, in the {murder_details[2]}")
    print("You have completed the tutorial!")
    
    return
    
#function pick_character
#This function gives the player an option to pick one of six chacters, then sends choice back to main
def pick_character(characters, non_player_character):
    count = 1 #Sets a count to 1
    non_player_character = [] #Create/set non_player_character to an empty list
    
    #For each item in the tuple characters
    for item in characters:
        #Print the count and the item, creating a list of characters to pick from
        print(f"{count}: {item}")
        count+=1
    
    #Assign a local variable that is the length of the tuple characters
    number_of_characters = int(len(characters))
      
    #Input, asking for the user to enter the number that matches the list above 
    choice = input_validation(f"Choose a character to play as from above list (enter 1-{number_of_characters}):    ", "numeric", len(characters))
    
    #for loop to check the entered value. If the number entered matches i, then they choice that location on the tuple - 1
    for i in range(number_of_characters+1):
        if choice == i:
            player_character = characters[i-1]
    
    #For loop to add the remaining characters to list non_player_characters. Checks to see if item from tuple is NOT player Character
    for item in characters:
        if item !=player_character:
            non_player_character.append(item)
    
    #Returns the chosen player character and the list of non player characters back to main
    return player_character, non_player_character
    
#function killer_file
#randomly chooses from six suspects, six weapons, and eight rooms
#Stores result in list
#Returns the new lists, missing the randomly chosen suspect, weapon, and room
def killer_file(suspects, weapons, rooms):
    #Create an empty list
    innocent_items = []
    
    murderer = suspects[random.randint(0, len(suspects)-1)]     #Randomly selects a suspect, using length of tuple as a parameter
    murder_weapon = weapons[random.randint(0, len(weapons)-1)]      #Randomly selects a weapon, using length of tuple as a parameter
    murder_location = rooms[random.randint(0, len(rooms)-1)]        #Randomly selects a room, using length of tuple as a parameter
    
    murder_details = [murderer, murder_weapon, murder_location]     #Creates a list of randomly chosen items 

    #for each item in suspects or weapons or rooms
    for item in suspects:
        #If that item is not in murder details, add the item to innocent items list
        if item != murder_details[0]:
            innocent_items.append(item)
        #if item not in murder details, add to innocent items
    for item in weapons:
        if item != murder_details[1]:
            innocent_items.append(item)
        #if item not in murder details, add to innocent items
    for item in rooms:
        if item != murder_details[2]:
            innocent_items.append(item)
            
    #returns to main
    return murder_details, innocent_items

#function knowledge_deal
#This "shuffles" the remaining suspects, weapons, and rooms
#Deal each item to each of the six players
def knowledge_deal(items, player, non_player):
    #shuffle the items and the non_player_characters so that they are in random
    random.shuffle(items)
    random.shuffle(non_player)
    
    #Determine how many items there are, divide that by the number of players to determine how many items each player knows
    number_of_cards_per_player = math.ceil(len(items) / ((len([player]) + len(non_player))))
    
    #Create a dictionary, with the key being the player's character and the value being a list of the items the player gets
    #The player gets the first items, the number of which is determined by number_of_cards_per_player
    player_hand = items[0:number_of_cards_per_player]
    
    #create an empty list, and start the count at the number of cards per player because the player already has the first items
    non_player_hands = {}
    count = number_of_cards_per_player
    
    #For each character in non_player
    for char in non_player:
        #That character's hand is a dictionary, where the key is the character name, and the value is a list
        #the value is from the items list, when the start is the current count, and the end is the count+number_of_cards_per_player
        char_hand = {char:items[count:count+number_of_cards_per_player]}
        #Update the non_player_hands dictionary with the new key:value pair
        non_player_hands.update(char_hand)
        #Add the number_of_cards_per_player to the current count
        count+=number_of_cards_per_player

    #Return the new dictionaries
    return player_hand, non_player_hands


#function question_answer
#This function is called after user chooses a room. It will prompt the user to make a guess
#It will then check against each of the other players cards to see if they have an item from the list
#It will store the answer given in a list known details
#It will store the question in a log called "past_queries", which can be accessed by user at beginning of question_answer
def question_answer(player_hand, non_player_hand, suspects, weapons, rooms):
    #Sets up a loop 
    move_on = False
    #While loop is not true
    while move_on != True:
        #Ask the user to select a suspect, a weapon, and a room
        question_suspect = input_validation("Pick one of the following suspects:", "alpha", suspects)
        question_weapon = input_validation("Pick one of the following weapons:", "alpha", weapons)
        question_room = input_validation("Pick one of the following rooms:", "alpha", rooms)

        #Inform the user about which items they have selected, and ask them if they are happy with their question
        print(), print(f"Your question is: {question_suspect}, with the {question_weapon}, in the {question_room}"),print()
        
        #Askes the user if they are happy with their question
        happy = input_validation("Are you happy with this as your question?", "alpha", ["Y", "N"])
        
        #If not happy, try again. Else move on
        if happy != "Y":
            print("You are not happy with your question. Let's try again:"), print()
        else:
            move_on = True
    
    print()
    #A loop to look at each item in the NPC hands to see if they have the item that matches it. 
    #for each character from the dictionary of NPC hands
    for char in non_player_hand.keys():
        print(f"{char} looks at their hand")
        #For each item in that NPC's hand
        for item in non_player_hand.get(char, "Nothing"):
            #If the item matches the suspect, inform the player and return the item
            if item in question_suspect:
                print(f"{char} has the suspect {item}!"), print()
                return item
            #If the item matches the weapon, inform the player and return the item
            elif item in question_weapon:
                print(f"{char} has the weapon {item}!"), print()
                return item 
            #If the item matches the room, inform the player and return the item
            elif item in question_room:
                print(f"{char} has the room {item}!"), print()
                return item 
        #If the NPC does not have the item, then inform the user        
        print(f"{char} does not have any of those items"), print()
    #If none of the characters have any of the items that were guessed, inform the user and return nothing
    print("Nobody at the table has any of those items!!!"), print()
    return False


#Function Tup To Dict
#Turns the tuples into dictionaries, used for the notepad function
def tup_to_dict(suspects, weapons, rooms):
    
    #Create an empty dictionary for each suspect, weapon, and room
    suspects_dict = {}
    weapons_dict = {}
    rooms_dict = {}
    
    #for each item in each of the tuples, turn it into a dictionary key with an empty value
    for item in suspects:
        pair = {item:" "}
        suspects_dict.update(pair)
    
    for item in weapons:
        pair = {item:" "}
        weapons_dict.update(pair)
    
    for item in rooms:
        pair = {item:" "}
        rooms_dict.update(pair)      

    #Return the new dictionaries
    return suspects_dict, weapons_dict, rooms_dict


#Function notepad
#Shows the user all their known information, as well as all the information they do not know
def notepad(player_hand, suspects, weapons, rooms):
    
    #For each item in the players hand (That they know about)
    for item in player_hand:
        #If that item is a key in any of the dictionaries suspects, weapons, or rooms, change the value to a X
        if item in suspects:
            update = {item: "X"}
            suspects.update(update)
            
        elif item in weapons:
            update = {item: "X"}
            weapons.update(update)
            
        elif item in rooms:
            update = {item: "X"}
            rooms.update(update)
        
    #Print a "notepad", or a list, showing an X next to any items that the user has uncovered as not in the murder file
    print(), print("     Suspects")
    print("-------------------")
    for item in suspects:
        print(f"{item:15}:{suspects.get(item)}")
    print()
    
    print("      Weapons")
    print("-------------------")
    for item in weapons: 
        print(f"{item:15}:{weapons.get(item)}")
    print()
    
    print("      Rooms")
    print("-------------------")
    for item in rooms:
        print(f"{item:15}:{rooms.get(item)}")
    print()
    

#function final_guess
#Asks user for their final suspect, weapon, and room. 
#Gives the user the chance to back out
#If right, tell them they won
#If wrong, tell them they lost and display correct result
def final_guess(murder_details, player_hand, non_player_characters_hand, suspects, weapons, rooms):
    #Commented out statement for testing purposes
    #print(),print(f"The murderer is {murder_details[0]}, with the {murder_details[1]}, in the {murder_details[2]}. "),print()

    #Sets up a loop 
    move_on = False
    #While loop is not true
    while move_on != True:
        #Ask the user to select a suspect, a weapon, and a room
        question_suspect = input_validation("Who is the murderer?:", "alpha", suspects)
        question_weapon = input_validation("What is the murder weapon?:", "alpha", weapons)
        question_room = input_validation("Where is the murder location?:", "alpha", rooms)

        #Inform the user about which items they have selected, and ask them if they are happy with their question
        print(), print(f"Your final accusation is: {question_suspect}, with the {question_weapon}, in the {question_room}"),print()
        
        #Askes the user if they are happy with their question
        happy = input_validation("Are you happy with this as your question?", "alpha", ["Y", "N"])
        
        #If not happy, try again. Else move on
        if happy != "Y":
            print("You are not happy with your question. Let's try again:"), print()
        else:
            #create a list of the user input, call it answer
            answer = [question_suspect, question_weapon, question_room]
            move_on = True
    
    print()
    #If the answer and murder details are identical, they have guessed correctly and the game is over. Victory
    if murder_details == answer:
        print(f"You are correct! The murderer is {murder_details[0]}, with the {murder_details[1]}, in the {murder_details[2]}. ")
        print("You have won the game!"), print()
    
    #if the answer and murder details are not identical, they have guess incorrectly and the game is over. Failure
    elif murder_details != answer:
        print(f"I'm sorry, that is incorrect. The murderer is {murder_details[0]}, with the {murder_details[1]}, in the {murder_details[2]}. ")
        print("You lose, better luck next time"), print()
    
    #Loop to show the rest of the NPC's hands
    print("The rest of the players at the table show their hands"), print()
    #For each character in the non player hand keys
    for char in non_player_characters_hand.keys():
        #Turn to a string and print out the items they know
        non_player_items = ", ".join(non_player_characters_hand[char])
        print(f"The character {char} knows the following items: {non_player_items}")
        
    return

#function menu
#Ask user to choose a room to go to
#Three options
#Option one: Make Guess. Calls 
#Option two: Look at known information. Displays information that the player knows, from items dealt originally to knowledge gained from guessing
#Option Three: Calls final guess. Calls final_guess function, ends game
def menu(murder_details, player_hand, non_player_hand, suspects, weapons, rooms):    
    
    #Turn the tuples into dictionaries. Used for the notepad function.
    suspects_dict, weapons_dict, rooms_dict = tup_to_dict(suspects, weapons, rooms)
    
    #Variable for while loop
    final_accusation = False
    
    #while the condition is not true, print a menu and ask user to choose an option from it
    while final_accusation != True:
        print("1: Ask a question to the list of suspects")
        print("2: Show notepad")
        print("3: Make final accusation"),print()
        menu_option = input_validation("Pick an option from the list above:    ", "numeric", MENU_LENGTH)
        
        #Option 1: Make an accusation. Calls the function question answer, returning the new information which will be added to the player's hand
        if menu_option == ASK_QUESTION:
            new_information = question_answer(player_hand, non_player_hand, suspects, weapons, rooms)
            #If the function does not return false, add this new information to players hand
            if new_information != False:
                player_hand.append(new_information)
        
        #Option 2: Call the notepad function, which prints a list of known and unknown detail for the user to see
        elif menu_option == SEE_NOTEPAD:
            notepad(player_hand, suspects_dict, weapons_dict, rooms_dict)
        
        #Option 3: Ask the user if they are sure, giving them the change to back out. This exits the loop
        #and ends the game
        elif menu_option == FINAL_GUESS:
            #Make sure the user wants to make their final guess
            double_check = input_validation("You are about to make your final accusation. This will end the game. Continue?    ", "alpha", ["Y", "N"])
            #If they want to make their final guess, exit loop and return to main
            if double_check == "Y":   
                final_accusation = True
                print("You are ready to make your final guess!")
            #If they don't, then stay in menu loop
            else:
                print("You do not want to make your final guess")
    
    return
            
def pre_game_assignments(suspects, weapons, rooms):
    non_player_characters = []#Empty list for non_player_characters to go to

    #Empty value for the while loop
    happy = "n"
    #While happy does not = Y
    while happy !="Y":
        #If happy does not = Y, call pick character function, which allows the user to pick their player character
        if happy != "Y":
            player_character, non_player_characters = pick_character(suspects, non_player_characters)
            
            #Inform user on who they have picked, and who they have not picked
            print(), print(f"You have chosen {player_character}!")
            #Ask user if they are happy with their choice
            happy = input_validation("Are you happy with your character choice?:", "alpha", ["Y", "N"])
            #If they are not happy, then repeat loop.
            if happy !="Y":
                print(),print("You are not happy with your character choice. Please pick again"), print()
        #if they are happy with their choice, then return their choice, as well as a list of the characters they did not choose
        else:
            return player_character, non_player_characters

    #Call killer_file, which chooses the murder weapon, the killer, and the murder location
    #returns list of items not in murder details
    murder_details, innocent_items_list = killer_file(suspects, weapons, rooms)
    
    #Flavor text to let the player know that the items have been delt
    print(), print("The deck of items is shuffled and delt to the players at the table.")
    
    #Call knowledge_deal, which takes all the innocent items are deals them randomly out
    player_hand, non_player_characters_hand = knowledge_deal(innocent_items_list, player_character, non_player_characters)
    
    #Tell the player what items they have in their hand
    print(f"You have the following items: {', '.join(player_hand)}"), print()
    
    #Return the murder details, the players hand, and the dictionaries of the NPC's hands
    return murder_details, player_hand, non_player_characters_hand


#main function
#Creates tuples of elements, which will be used throughout the game
#greet user, outline game, explain tutorial.
#call pre_game_assignments
def main():
    #create tuples of: suspects, weapons, and rooms
    suspects = ("Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum")
    weapons = ("Wrench", "Candlestick", "Lead Pipe", "Rope", "Revolver", "Knife")
    rooms = ("Kitchen", "Ball Room", "Conservatory", "Dinning Room", "Lounge", "Billard Room", "Library", "Study")

    play_again = "Y"
    while play_again != "N":
        
        #Print short message. This will be replaced with a tutorial soon
        print("Welcome to the game of Clue! A murder has occured in the mansion. Solve it by asking a series of questions to determine which person knows what!")
        print("The game ends when you have determined the murderer, the weapon, and the murder location"), print()
        
        #Askes the user if they would like to play the tutorial
        play_tutorial = input_validation("Would you like to see the tutorial?:   ", "alpha", ["Y", "N"])
        
        #If they answer yes, call tutorial, then ask them if they want to see the tutorial again
        while play_tutorial == "Y":
            tutorial()
            play_tutorial = input_validation("Would you like to see the tutorial again?:   ", "alpha", ["Y", "N"]) 
        
        #If they say no, then begin the game.
        print(), print("Okay then, let's... Begin!")
        
        #Call pre_game_assignments. This sets up all the information needed to play a round
        murder_details, player_hand, non_player_characters_hand = pre_game_assignments(suspects, weapons, rooms)
        
        #The game loop:
        #Call menu, which has all the options for the user to pick from
        menu(murder_details, player_hand, non_player_characters_hand, suspects, weapons, rooms)
        
        #Call final guess, where the user will make their final accusation
        final_guess(murder_details, player_hand, non_player_characters_hand, suspects, weapons, rooms)
        
        #Ask them if they want to play again
        play_again = input_validation("Play again?:   ", "alpha", ["Y", "N"])
        
        #If play again is N, thank the user for playing and exit loop
        if play_again == "N":
            print(), print("Okay, thanks for playing!")
            
main()
