'''
Noah Walton
IS 303 - A02

Quest Recommender
This program recommends quests based on player level and player class.
Different quests for level ranges (1-10, 11-25, 26+), modified by class (warrior, mage, rogue)

Inputs:
- Player name (string)
- Player level (integer)
- Player class (string)

Processes:
- Validate level (must be positive)
- Validate class (must be one of the supported classes)
- Determine quest difficulty based on level
- Recommend quests based on class and difficulty

Outputs:
- Print recommended quests
- Print error message if any input is invalid
'''

print("Welcome to the Quest Recommender!")

#Input: Get player information
player_name = input("Enter your name: ")
player_level = int(input("Enter your level (1-35): "))
if player_level < 1 or player_level > 35:
    print("Error: Please enter a level between 1 and 35.")
else:
    player_class = input("Enter your class (warrior, mage, rogue): ").lower()
    if player_class not in ["warrior", "mage", "rogue"]:
        print("Error: Please enter 'warrior', 'mage', or 'rogue'.") 
    else:
        #Process: Determine quest difficulty
        if player_level <= 10:
            difficulty = "easy"
        elif player_level <= 25:
            difficulty = "medium"
        else:
            difficulty = "hard"
        #Recommend quests based on class and difficulty
        if player_class == "warrior":
            if difficulty == "easy":
                quests = ["Defend the Village of Whiterum", "Stop the Blood Enraged Boar"]
            elif difficulty == "medium":
                quests = ["Guard the Caravan of Cortallin", "Slay the Black Cloaked Bandits"]
            else:
                quests = ["Conquer the Forged Fortress", "Defeat the Dragon Athetusis"]
        elif player_class == "mage":
            if difficulty == "easy":
                quests = ["Collect Herbs", "Study Ancient Texts in the Library of Eldenate"]
            elif difficulty == "medium":
                quests = ["Investigate Magical Disturbances", "Defeat the Sorcerer in the Cursed Tower in the North."]
            else:
                quests = ["Seal the Demon Portal", "Master the Arcane"]
        else:  # rogue
            if difficulty == "easy":
                quests = ["Pickpocket Tetreth the Merchant", "Enter the Tavern and Steal the key to the Armory"]
            elif difficulty == "medium":
                quests = ["Infiltrate the Bandit Camp", "Steal the Artefact at night"]
            else:
                quests = ["Assassinate the Warlord Weldethin", "Steal the Crown Jewels"]

        #Output: Print recommended quests
        print(f"Recommended quests for {player_name} (Level {player_level} {player_class.capitalize()}):")
        for quest in quests:
            print(f"- {quest}")
        print(f"Good luck on your adventures, {player_name} the {player_class.capitalize()}!")
