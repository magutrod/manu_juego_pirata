import random
import os
from datetime import datetime

'''
File Docstring:
Author: Manuel Gutierrez Payan
Description: This is a text-based adventure game where the player explores an Island, loots zones, and avoids a terrifying Pirate.
Game features:
1. The player starts at the beach and can navigate to the connected zones which are displayed in the menu.
2. Player can loot the landing zone and earn random coins from a loot table assigned to each zone.
3. Pirate randomly moves to a different zone when player moves to a new zone.
4. Player loses the game if the Pirate and the player are in the same zone`.
5. The player wins the game by finding and escaping to the exit zone with the accumulated loot.
Challenges implemented:
1. Each zone has a loot table. When the player loots a zone, they have a chance to receive an item specific to that zone with a fixed value.
2. Secret Treasure. When the player loots a zone, they have a small chance to find a Treasure. The player receives a bonus to their score.
3. Top 10 scores Leaderboard. The ten higher scores are written to a file, and once the game ends, the top ten scores are printed to the screen.
'''

islandZones = {
    "beach": {
        "description": "You are at the beach. You can see a volcano, the jungle, and a mysterious cave.",
        "connections": ["volcano", "jungle", "mysterious cave"],
        "loot_table": [0, 5, 10],
        "hiddenTreasure": 0.1,
        "treasureLoot": [15, 25] 
    },
    "volcano": {
        "description": "You are near an active volcano. The ground is hot, and there's a path leading to the beach and the jungle.",
        "connections": ["beach", "jungle","exit"],
        "loot_table": [0, 5, 15],
        "hiddenTreasure": 0.05,
        "treasureLoot": [20, 30] 
    },
    "jungle": {
        "description": "You are deep in the jungle. The trees are thick, and there are paths to the volcano, beach, and mysterious cave.",
        "connections": ["beach", "volcano", "mysterious cave"],
        "loot_table": [1, 3, 7],
        "hiddenTreasure": 0.15,
        "treasureLoot": [8, 16] 
    },
    "mysterious cave": {
        "description": "You are inside a mysterious cave. The walls echo with strange sounds. There's a path leading to the jungle and the beach.",
        "connections": ["beach", "jungle"],
        "loot_table": [0, 10, 20],
        "hiddenTreasure": 0.2,
        "treasureLoot": [7, 14] 
    },
    "treasure cove": {
        "description": "You are at a hidden treasure cove, where the sand is golden and the waves crash gently. There's a way to the jungle and the beach.",
        "connections": ["beach", "jungle","exit"],
        "loot_table": [10, 15, 20],
        "hiddenTreasure": 0.1,
        "treasureLoot": [15, 25] 
    },
    "hidden temple": {
        "description": "You stand before an ancient temple, its entrance surrounded by overgrown vines. The jungle path leads here.",
        "connections": ["jungle"],
        "loot_table": [0, 2, 5],
        "hiddenTreasure": 0.25,
        "treasureLoot": [5, 10] 
    },
    "pirate ship": {
        "description": "You've discovered an old pirate ship stranded on the shore. It's said to have great loot hidden aboard.",
        "connections": ["beach"],
        "loot_table": [1, 3, 7],
        "hiddenTreasure": 0.1,
        "treasureLoot": [15, 25] 
    },
    "coral reef": {
        "description": "You are at a vibrant coral reef. Colorful fish swim around, and there are paths leading to the beach and the pirate ship.",
        "connections": ["beach", "pirate ship"],
        "loot_table": [0, 2, 6],
        "hiddenTreasure": 0.06,
        "treasureLoot": [20, 30] 
    },
    "exit": {
        "description": "You have found the exit of the island! You've successfully made it off the island, with your loot in hand. You are free!",
        "connections": [],
        "loot_table": [0],
        "hiddenTreasure": 0,
        "treasureLoot": [] 
    },
    "abandoned lighthouse": {
        "description": "You stand before an old, abandoned lighthouse. The light no longer shines, but there's a path leading to the beach and the jungle.",
        "connections": ["beach", "jungle"],
        "loot_table": [0, 4, 7],
        "hiddenTreasure": 0.03,
        "treasureLoot": [20, 30] 
    },
    "cliffside": {
        "description": "You are at the edge of a high cliff overlooking the ocean. There's a dangerous path down to the treasure cove, and another path leads to the volcano.",
        "connections": ["treasure cove", "volcano","exit"],
        "loot_table": [0, 5, 10],
        "hiddenTreasure": 0.12,
        "treasureLoot": [10, 15] 
    },
    "hidden lagoon": {
        "description": "You find yourself in a serene, hidden lagoon surrounded by tall cliffs. The water is crystal clear. The jungle and coral reef are nearby.",
        "connections": ["jungle", "coral reef"],
        "loot_table": [0, 5, 12],
        "hiddenTreasure": 0.25,
        "treasureLoot": [5, 10] 
    }
}

# Global variables
playerCoins = 0
playerZone = "beach"
pirateZone= random.choice([zone for zone in islandZones if zone != "beach" and zone != "exit"])

def game():
    '''
    This function starts the game loop and initializes the game state.
    Game finishes when the player decides to exit or when the player and the pirate are in the same zone
    '''
    print("\nWelcome to The Island. The Island was abandoned many years ago. Legend says that there are many treasures burried waiting to be taken. However, other legends say that a fearsome pirate lurks through the island zones. Will you escape with valuable loot or be killed by the terrifying Pirate?\n")

    # Ask player to enter a name
    playerName = input("Enter your name: ").strip()

    while True:
        print("\n"+islandZones[playerZone]["description"])
        print(f"You currently have {playerCoins} coins.")
        print(f"The Pirate is in a nearby zone...")
        print("\nZones: \n" + "\t"+"\n\t".join(islandZones[playerZone]["connections"]))

        if playerZone == "exit":
            print("Actions: \n\tmove [zone]\n\tloot\n\texit")
        else:
            print("Actions: \n\tmove [zone]\n\tloot")
       
        playerAction = processInput()
        if playerAction == "exit":
            print(f"You wisely decided to leave the Pirate to its Island.")
            print(f"\nYour final score: {playerCoins}")
            break

    # Save the player's score if it is among the top 10
    saveHighScore(playerCoins, playerName)

    # Display the top 10 high scores
    displayHighScores()

def processInput():
    '''
    This function handles the input from the player and executes the player's action.
    It returns a string with the action that the player wants to take.
    '''
    while True:
        action = input(">> ").strip().lower()

        if action.startswith("move"):
            destination = action[5:].strip()
            if destination in islandZones[playerZone]["connections"]:
                movePlayer(destination)
                return
            else:
                print("Error: Invalid Action")
        
        elif action == "loot":
            lootZone()
            return
        
        elif action == "exit":
            return "exit"
        
        else:
            print("Error: Invalid Action")

def movePlayer(destination):
    '''
    This function moves the player to a new zone, updates the game state, and checks for the Pirate zone.
    '''
    global playerZone
    playerZone = destination
    update()

def lootZone():
    '''
    This function handles looting a zone and checking if loot was found. It also checks for proximity to the Pirate.
    '''
    global playerCoins

    loot = random.choice(islandZones[playerZone]["loot_table"])
    playerCoins += loot
    
    if playerZone == "exit":
        print("You are at the exit zone. There is nothing to loot here!")
    elif loot > 0:
        print(f"You found {loot} coins!")
    else:
        print("You didn't find anything.")

     # Secret zone chance
    if random.random() < islandZones[playerZone]["hiddenTreasure"]:
        print(f"You discovered a Hidden Treasure!")
        
        # Add bonus loot for discovering a secret zone
        secretLoot = random.choice(islandZones[playerZone]["treasureLoot"])
        print(f"The Hidden Treasure has {secretLoot} bonus loot!")
        playerCoins += secretLoot
    
    update()

def update():
    '''
    This function moves the Pirate, checks if the game is over, and updates the Pirate' status.
    '''
    global pirateZone

    pirateZone= random.choice([zone for zone in islandZones if zone != "beach" and zone != "exit"])

    if pirateZone == playerZone:
        print("The Pirate has found you! You drop everything and flee the Island.")
        # Display the top 10 high scores
        displayHighScores()
        exit()
    
    if pirateZone in islandZones[playerZone]["connections"]:
        print("You hear the Pirate lurking.")

def loadHighScores():
    """
    This function loads the top 10 high scores from the 'high_scores.txt' file and then return
    them as a tuple (score, player name)
    """
    if not os.path.exists("high_scores.txt"):
        return []
    
    with open("high_scores.txt", "r") as file:
        scores = [line.strip() for line in file.readlines()]
    
    # Convert scores to a list of tuples (score, playerName)
    high_scores = []
    for score in scores:
        score, name  = score.split(", ")
        high_scores.append((int(score), name ))
    
    # Return top 10 scores with higher score at the top
    return sorted(high_scores, reverse=True)[:10]  

def saveHighScore(score, playerName):
    """
    This function saves a new player's score to the 'high_scores.txt' file.
    Parameters received are the accumulated player coins (score) and the player name
    """

    high_scores = loadHighScores()

    # Append the new score
    high_scores.append((score, playerName))
    # Keep top 10 scores
    high_scores = sorted(high_scores, reverse=True)[:10]  
    
    with open("high_scores.txt", "w") as file:
        for score, name in high_scores:
            file.write(f"{score}, {name}\n")

def displayHighScores():
    """
    This function displays the top 10 high scores.
    """
    high_scores = loadHighScores()
    
    if high_scores:
        print("\nTop 10 High Scores:")
        for i, (score, name) in enumerate(high_scores, 1):
            print(f"{i}. {name}: {score}")
    else:
        print("\nNo high scores yet!")

# Start the game
game()
