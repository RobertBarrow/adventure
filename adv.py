#! python
from sys import stdout
import random
import time

DEBUG = False # True
SUSPENSE_LEVEL = 0.1

LEVEL = 0
NPC = 0

QUIT = False
PLAY = True
FIGHT = False
BRIBE = False

weapons = {'knife':{'image':"asciiart/knife"}, 'axe':{'image':"asciiart/axe"}}

characters = {}

def outcome(probability):
    return random.random() < probability

def display_weapon(weapon):
    if len(weapons[weapon]['image']) > 0: # display the ascii art for the weapon
        image_file=open(weapons[weapon]['image'])
        print(image_file.read())
        image_file.close()

def display_asciiart(image):
    image_file=open('asciiart/'+image, 'rU', encoding='ansi')
    print(image_file.read())
    image_file.close()

def attack(attacking, defending):
    if outcome(characters[attacking]['hit']):
        if outcome(characters[defending]['block']):
            if characters[defending]['shield'] > 0:
                display_asciiart('shield')
            else:
                display_asciiart('blocked')
            return "Blocked!"
        else:
            display_asciiart('strike')
            if characters[attacking]['weapon']:
                display_weapon(characters[attacking]['weapon'])
            event = ''
            damage = random.randint(1, characters[attacking]['strength'])
            if characters[defending]['shield'] > damage:
                characters[defending]['shield'] -= damage
                event += "Shield depletion: " + str(damage) + " ... "
            else:
                if characters[defending]['shield'] > 0:
                    damage -= characters[defending]['shield']
                    characters[defending]['shield'] = 0
                    event += defending + " lost their shield ... "
                    characters[defending]['block'] -= 0.1
                    display_asciiart('broken_shield') # display the broken shield ascii art
                if characters[defending]['health'] > damage:
                    characters[defending]['health'] -= damage
                    event += "Health depletion: " + str(damage) + " ... "
                else:
                    characters[defending]['health'] = 0
                    characters[defending]['status'] = "dead" 
                    event += "It\'s a fatal blow! ... " + defending +  " is dead! ... "
                    if characters[defending]['gold']:
                        display_asciiart('gold')
                        event += attacking + " takes " + str(characters[defending]['gold']) + " gold ... "
                        characters[attacking]['gold'] += characters[defending]['gold'] # pick up their gold
                        characters[defending]['gold'] = 0
                    if characters[defending]['healing']:
                        event += attacking + " takes the healing potion ... "
                        characters[attacking]['healing'] += characters[defending]['healing'] # pick up their healing potion
                        characters[defending]['healing'] = 0
                    if characters[defending]['weapon']:
                        if characters[attacking]['weapon'] == False:
                            weapon = characters[defending]['weapon']
                            display_weapon(weapon)
                            event += attacking + " takes the " + weapon + " ... "
                            characters[attacking]['weapon'] = weapon # pick up their weapon
                            characters[attacking]['hit'] += 0.1 # attack bonus
                        characters[defending]['weapon'] = False
            return "Strike! ... " + event
    else:
        return "Miss!"

def create_character(name, weapon, shield):
    characters[name] = {}
    characters[name]['weapon'] = weapon
    characters[name]['health'] = random.randint(50, 100)
    characters[name]['gold'] = random.randint(0, 100)
    characters[name]['healing'] = random.randint(0,50)
    characters[name]['status'] = "alive"

    if weapon:
        if outcome(0.5):
            characters[name]['weapon'] = "axe"
            characters[name]['strength'] = random.randint(30,60)
            characters[name]['hit'] = random.randint(30,90) / 100
        else:
            characters[name]['weapon'] = "knife"
            characters[name]['strength'] = random.randint(20,50)
            characters[name]['hit'] = random.randint(20,90) / 100
    else:
        characters[name]['strength'] = random.randint(10,40)
        characters[name]['hit'] = random.randint(10,80) / 100
   
    if shield:
        characters[name]['shield'] = random.randint(0, 50)
        characters[name]['block'] = random.randint(10,80) / 100
    else:
        characters[name]['shield'] = 0
        characters[name]['block'] = random.randint(0,70) / 100
    return name
    
def status(key):
    print(f"\n{key}:\t")
    print(f"\tStrength:\t{characters[key]['strength']}", end=" ")
    if characters[key]['weapon']:
        print(f"\tWeapon:\t{characters[key]['weapon']}" ,end=" ")
    else:
        print(f"\tWeapon:\tN/A" ,end=" ")
    print(f"\tHit ratio:\t{characters[key]['hit']:.2f}", end=" ") # {0:.2f}
    #print(f"\tStatus:\t{characters[key]['status']}", end=" ")
    print(f"\tGold:\t{characters[key]['gold']:.0f}", end="\n")
    print(f"\tHealth:\t\t{characters[key]['health']}", end=" ")
    print(f"\tShield:\t{characters[key]['shield']}", end=" ")
    print(f"\tBlock ratio:\t{characters[key]['block']:.2f}", end=" ")
    print(f"\tHealing potion:\t{characters[key]['healing']}")

def heal_team():
    for player in team:
        if characters[player]['healing']:
            print(player + " drinks healing potion to restore their health ...")
            characters[player]['health'] += characters[player]['healing']
            characters[player]['healing'] = 0
            if characters[player]['health'] > 100:
                characters[player]['healing'] = characters[player]['health'] - 100 # remaining health potion
                characters[player]['health'] = 100
            add_suspense()

def add_suspense():
    if DEBUG == False:
        stdout.flush()
        time.sleep(SUSPENSE_LEVEL)
    
team = [create_character("Player " + str(p), outcome(0.6), outcome(0.6)) for p in range(1,random.randint(2,5))]

if DEBUG: print("Characters: " + format(characters))
if DEBUG: print("Team: " + format(team))


display_asciiart('castle')

while team and QUIT == False:

    add_suspense()

    print("\nYou are currently in LEVEL " + str(LEVEL) + " ... ")

    print("\nYour team\'s status:")
    for player in team:
        status(player)

    add_suspense()
    print("\nPress ENTER to continue\n")  
    input()

    add_suspense()

    if outcome(0.2): # 20% chance of spawning a MONSTER
        if outcome(0.1): # 1 in 10 chance of spawning a DEMON
            horde = [create_character("Demon", False, False)]
            display_asciiart('demon')
        elif outcome(0.1): # 1 in 10 chance of spawning a DRAGON
            horde = [create_character("Dragon", False, False)]
            display_asciiart('dragon')
        elif outcome(0.1): # 1 in 10 chance of spawning a GIANT ANT
            horde = [create_character("Giant ant", False, False)]
            display_asciiart('giant_ant')
        elif outcome(0.1): # 1 in 10 chance of spawning a CYCLOPS
            horde = [create_character("Snake", False, False)]
            display_asciiart('snake')
        elif outcome(0.1): # 1 in 10 chance of spawning a CYCLOPS
            horde = [create_character("Cyclops", False, False)]
            display_asciiart('cyclops')
        else: # spawn 3 BATS
            horde = [create_character("Bat " + str(h), False, False) for h in range(NPC, NPC + 3)]
            NPC += 3
            display_asciiart('bats')
    else: # just spawn a horde of skeletons
        horde_size = random.randint(1,3)
        horde = [create_character("Skeleton " + str(h), outcome(0.4), outcome(0.4)) for h in range(NPC, NPC + horde_size)]
        NPC += horde_size
        display_asciiart('skeleton')

    if DEBUG:
        for npc in horde:
            status(npc)

    add_suspense()  

    FIGHT = False
    BRIBE = False

    decision = input("\nF to fight, B to bribe, Q to quit\t")

    if decision == 'F' or decision == 'f': FIGHT = True
    if decision == 'B' or decision == 'b': BRIBE = True
    if decision == 'Q' or decision == 'q': 
        QUIT = True
        break
    
    add_suspense()

    if BRIBE: 
        if DEBUG: print("Team: " + format(team))
        display_asciiart('gold')
        for player in team:
            if DEBUG: print("Player: " + format(player))
            if BRIBE: 
                for npc in horde:
                    if DEBUG: print("Horde NPC: " + format(npc))
                    if characters[player]['gold']:
                        bribe = random.randint(1,characters[player]['gold'])
                        if BRIBE:
                            print(player + " pays " + str(bribe) + " gold to " + npc + " ... ")
                            characters[player]['gold'] -= bribe
                            add_suspense()
                    else:
                        print("\aThere is not enough gold! ... You will have to fight them! ")
                        BRIBE = False
                        FIGHT = True
                        add_suspense()
                        break
        LEVEL += 1
        display_asciiart('passage')

    if FIGHT:
        add_suspense()
        print("\nBATTLE COMMENCES ...\n")
        add_suspense()
        while team and horde:
            for player in team:
                for npc in horde:
                    if characters[player]['status'] == 'alive' and characters[npc]['status'] == 'alive':
                        print(f"{player} attacks {npc} :", end=" ")
                        add_suspense()
                        print (f"{attack(player, npc)}")
                        add_suspense()                    
                    if characters[npc]['status'] == 'alive' and characters[player]['status'] == 'alive':
                        print(f"{npc} attacks {player} :", end=" ")
                        if characters[npc]['weapon'] == "knife":
                            display_asciiart('skeleton_attacks')
                        add_suspense()
                        print(f"{attack(npc, player)}")
                        add_suspense()
            for player in team:
                if characters[player]['status'] == 'dead':
                    team.remove(player)
            for npc in horde:
                if characters[npc]['status'] == 'dead':
                    horde.remove(npc)
        
        add_suspense()            
        print(f"\nOUTCOME:\n")
        add_suspense()

        if team:            
            print("Your team was victorious!!!\n")
            add_suspense()
            heal_team()
            LEVEL += 1
            display_asciiart('passage')
            print("You continue on to the next room ...\n")
        else:
            print("Your team was defeated!!!\n")
            add_suspense()

GOLD = 0
for player in team:
    GOLD += characters[player]['gold']

if GOLD:
    print("Your team escaped from level " + str(LEVEL) + " with " + str(GOLD) + " gold.\n")

if DEBUG: 
    for key, value in characters.items() :
        print (key, value)



