#! python
from os import environ
from sys import stdout
import random
import time
import inflect
import adv_functions as adv

# DEBUG_MODE = False
# Enable debugging if the DEBUG environment variable is set and starts with Y
DEBUG_MODE = environ.get("DEBUG", "").lower().startswith('y') or environ.get("DEBUG", "").lower().startswith('t')

SUSPENSE_LEVEL = 0.1
LEVEL = 1
GRIDREF = "D7"
QUIT = False
FIGHT = False
BRIBE = False

team = [adv.create_character("Player " + str(p), adv.outcome(0.6), 70, adv.outcome(0.6), 0) for p in range(1,random.randint(2,5))]

if DEBUG_MODE: 
    print("DEBUG_MODE=" + format(DEBUG_MODE))
    print("Characters: " + format(adv.characters))
    print("Team: " + format(team))
    print("Weapons: " + format(adv.weapons))
    print("Monsters: " + format(adv.monsters))
    print("Map locations: " + format(adv.map_locations))
else: 
    adv.chapter_text(LEVEL, "intro")
    adv.display_asciiart("castle")

while team and QUIT == False:

    if DEBUG_MODE:
        for key, value in adv.characters.items():
            print (key, value)
    else:
        print("\nYou are currently in LEVEL " + str(LEVEL) + ", GRIDREF " + GRIDREF + " ... " + format(adv.map_locations["ValidLevels"][str(LEVEL)]["ValidGridRefs"][GRIDREF]['name']))
        print("\nExits: ")
        for exit in adv.map_locations["ValidLevels"][str(LEVEL)]["ValidGridRefs"][GRIDREF]['exits']:
            visible_gridref = adv.map_locations["ValidLevels"][str(LEVEL)]["ValidGridRefs"][GRIDREF]['exits'][exit]
            print("\n\t" + format(exit) + " - " + format(adv.map_locations["ValidLevels"][str(LEVEL)]["ValidGridRefs"][visible_gridref]['name']))
        print("\nYour team\'s status:")
        for player in team:
            adv.status(player)

    adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
    print("\nPress ENTER to continue\n")  
    input()

    adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
    horde = adv.generate_horde()
    if DEBUG_MODE: 
        for npc in horde:
            print(format(npc))
    else:
        adv.display_horde(horde)
        for npc in horde:
            adv.status(npc)

    FIGHT = False
    BRIBE = False
    adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
    decision = input("\nF to fight, B to bribe, Q to quit\t")

    if decision == 'F' or decision == 'f': FIGHT = True
    if decision == 'B' or decision == 'b': BRIBE = True
    if decision == 'Q' or decision == 'q': 
        QUIT = True
        break
    
    adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)

    if BRIBE:
        if adv.bribe(team, horde, DEBUG_MODE):
            adv.display_asciiart('passage')
        else:
            FIGHT = True

    if FIGHT:
        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
        print("\nBATTLE COMMENCES ...\n")
        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
        while team and horde:
            for player in team:
                for npc in horde:
                    if adv.characters[player]['status'] == 'alive' and adv.characters[npc]['status'] == 'alive':
                        if DEBUG_MODE:
                            print(f"{player} attacks {npc} :", end=" ")
                            print (f"{adv.attack(player, npc)}")
                        else:
                            adv.talk(player + " attacks " + npc + " : ")
                            adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
                            adv.talk(adv.attack(player, npc))
                            adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)                    
                    if adv.characters[npc]['status'] == 'alive' and adv.characters[player]['status'] == 'alive':
                        print(f"{npc} attacks {player} :", end=" ")
                        if adv.characters[npc]['weapon'] == "knife":
                            adv.display_asciiart('skeleton_attacks')
                        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
                        print(f"{adv.attack(npc, player)}")
                        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
            for player in team:
                if adv.characters[player]['status'] == 'dead':
                    team.remove(player)
            for npc in horde:
                if adv.characters[npc]['status'] == 'dead':
                    horde.remove(npc)
        
        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)           
        print(f"\nOUTCOME:\n")
        adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)

        if team:            
            print("Your team was victorious!!!\n")
            adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)
            adv.heal_team(team)
            LEVEL += 1
            adv.display_asciiart('passage')
            print("You continue on to the next room ...\n")
        else:
            print("Your team was defeated!!!\n")
            adv.add_suspense(SUSPENSE_LEVEL, DEBUG_MODE)

GOLD = 0
for player in team:
    GOLD += adv.characters[player]['gold']

if GOLD:
    print("Your team escaped from level " + str(LEVEL) + " with " + str(GOLD) + " gold.\n")

if DEBUG_MODE: 
    for key, value in adv.characters.items() :
        print (key, value)