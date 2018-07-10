#! python
from sys import stdout
import random
import inflect
import adv_functions as adv

DEBUG = False # True

LEVEL = 1
NPC = 0

QUIT = False
PLAY = True
FIGHT = False
BRIBE = False
  
team = [adv.create_character("Player " + str(p), adv.outcome(0.6), adv.outcome(0.6)) for p in range(1,random.randint(2,5))]

if DEBUG: print("Characters: " + format(adv.characters))
if DEBUG: print("Team: " + format(team))

adv.chapter_text(LEVEL, "intro")
adv.display_asciiart('castle')

while team and QUIT == False:

    adv.add_suspense()

    if DEBUG: 
        print("\nYou are currently in LEVEL " + str(LEVEL) + " ... ")
    
    print("\nYour team\'s status:")
    for player in team:
        adv.status(player)

    adv.add_suspense()
    print("\nPress ENTER to continue\n")  
    input()

    adv.add_suspense()

    if adv.outcome(0.2): # 20% chance of spawning a MONSTER
        if adv.outcome(0.1): # 1 in 10 chance of spawning a DEMON
            horde = [adv.create_character("Demon", False, False)]
            adv.display_asciiart('demon')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a DRAGON
            horde = [adv.create_character("Dragon", False, False)]
            adv.display_asciiart('dragon')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a GIANT ANT
            horde = [adv.create_character("Giant ant", False, False)]
            adv.display_asciiart('giant_ant')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a CYCLOPS
            horde = [adv.create_character("Snake", False, False)]
            adv.display_asciiart('snake')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a CYCLOPS
            horde = [adv.create_character("Cyclops", False, False)]
            adv.display_asciiart('cyclops')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a GARGOYLE
            horde = [adv.create_character("Gargoyle", False, False)]
            adv.display_asciiart('gargoyle')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a GOBLIN
            horde = [adv.create_character("Goblin", False, False)]
            adv.display_asciiart('goblin')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a SPIDER
            horde = [adv.create_character("Spider", False, False)]
            adv.display_asciiart('spider')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a WOLF
            horde = [adv.create_character("Wolf", False, False)]
            adv.display_asciiart('wolf')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a SCORPION
            horde = [adv.create_character("Scorpion", False, False)]
            adv.display_asciiart('scorpion')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a OGRE
            horde = [adv.create_character("Ogre", False, False)]
            adv.display_asciiart('ogre')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a MINOTAUR
            horde = [adv.create_character("Minotaur", False, False)]
            adv.display_asciiart('minotaur')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a HORSEMAN
            horde = [adv.create_character("Horseman", False, False)]
            adv.display_asciiart('horseman')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a KNIGHT
            horde = [adv.create_character("Knight", False, False)]
            adv.display_asciiart('knight')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a MEDUSA
            horde = [adv.create_character("Medusa", False, False)]
            adv.display_asciiart('medusa')
        elif adv.outcome(0.1): # 1 in 10 chance of spawning a CERBERUS
            horde = [adv.create_character("Cerberus", False, False)]
            adv.display_asciiart('cerberus')
        else: # spawn 3 BATS
            horde = [adv.create_character("Bat " + str(h), False, False) for h in range(NPC, NPC + 3)]
            NPC += 3
            adv.display_asciiart('bats')
    else: # just spawn a horde of skeletons
        horde_size = random.randint(1,3)
        horde = [adv.create_character("Skeleton " + str(h), adv.outcome(0.4), adv.outcome(0.4)) for h in range(NPC, NPC + horde_size)]
        NPC += horde_size
        adv.display_asciiart('skeleton')

    if DEBUG:
        for npc in horde:
            adv.status(npc)

    adv.add_suspense()  

    FIGHT = False
    BRIBE = False

    decision = input("\nF to fight, B to bribe, Q to quit\t")

    if decision == 'F' or decision == 'f': FIGHT = True
    if decision == 'B' or decision == 'b': BRIBE = True
    if decision == 'Q' or decision == 'q': 
        QUIT = True
        break
    
    adv.add_suspense()

    if BRIBE: 
        if DEBUG: print("Team: " + format(team))
        adv.display_asciiart('gold')
        for player in team:
            if DEBUG: print("Player: " + format(player))
            if BRIBE: 
                for npc in horde:
                    if DEBUG: print("Horde NPC: " + format(npc))
                    if adv.characters[player]['gold']:
                        bribe = random.randint(1,adv.characters[player]['gold'])
                        if BRIBE:
                            print(player + " pays " + str(bribe) + " gold to " + npc + " ... ")
                            adv.characters[player]['gold'] -= bribe
                            adv.add_suspense()
                    else:
                        print("\aThere is not enough gold! ... You will have to fight them! ")
                        BRIBE = False
                        FIGHT = True
                        adv.add_suspense()
                        break
        #LEVEL += 1
        adv.display_asciiart('passage')

    if FIGHT:
        adv.add_suspense()
        print("\nBATTLE COMMENCES ...\n")
        adv.add_suspense()
        while team and horde:
            for player in team:
                for npc in horde:
                    if adv.characters[player]['status'] == 'alive' and adv.characters[npc]['status'] == 'alive':
                        print(f"{player} attacks {npc} :", end=" ")
                        adv.add_suspense()
                        print (f"{adv.attack(player, npc)}")
                        adv.add_suspense()                    
                    if adv.characters[npc]['status'] == 'alive' and adv.characters[player]['status'] == 'alive':
                        print(f"{npc} attacks {player} :", end=" ")
                        if adv.characters[npc]['weapon'] == "knife":
                            adv.display_asciiart('skeleton_attacks')
                        adv.add_suspense()
                        print(f"{adv.attack(npc, player)}")
                        adv.add_suspense()
            for player in team:
                if adv.characters[player]['status'] == 'dead':
                    team.remove(player)
            for npc in horde:
                if adv.characters[npc]['status'] == 'dead':
                    horde.remove(npc)
        
        adv.add_suspense()            
        print(f"\nOUTCOME:\n")
        adv.add_suspense()

        if team:            
            print("Your team was victorious!!!\n")
            adv.add_suspense()
            adv.heal_team(team)
            LEVEL += 1
            adv.display_asciiart('passage')
            print("You continue on to the next room ...\n")
        else:
            print("Your team was defeated!!!\n")
            adv.add_suspense()

GOLD = 0
for player in team:
    GOLD += adv.characters[player]['gold']

if GOLD:
    print("Your team escaped from level " + str(LEVEL) + " with " + str(GOLD) + " gold.\n")

if DEBUG: 
    for key, value in adv.characters.items() :
        print (key, value)



