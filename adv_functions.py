#! python
from sys import stdout
from os import system
import random
import time

import inflect
inflect = inflect.engine()

characters = {}
weapons = {'knife':{'image':"asciiart/knife"}, 'axe':{'image':"asciiart/axe"}}

def outcome(probability):
    return random.random() < probability

def display_weapon(weapon):
    if len(weapons[weapon]['image']) > 0: # display the ascii art for the weapon
        image_file=open(weapons[weapon]['image'])
        print(image_file.read())
        image_file.close()

def display_asciiart(image):
    image_file=open('asciiart/'+image, 'rU', encoding='latin1')
    print(image_file.read())
    image_file.close()

def display_text_file(filename):
    text_file=open('text/'+filename, 'rU', encoding='latin1')
    for line in text_file:
        if line.startswith("text "):
            print(line[5:])
        elif line.startswith("talk "):
            talk = line[5:]
            for char in talk:
                stdout.write(char)
                stdout.flush()
                time.sleep(0.05)
        elif line.startswith("pause "):
            pause = int(line[6:].rstrip())
            time.sleep(pause)
        elif line.startswith("ascii "):
            display_asciiart(line[6:].rstrip())
        elif line.startswith("continue"):
            input("Press RETURN to continue...")
        elif line.startswith("clear"):
            system('clear')
        stdout.flush()
    text_file.close()

def chapter_text(level, sub_level):
    chapter_text = "chapter_" + inflect.number_to_words(level) + "_" + sub_level
    display_text_file(chapter_text)

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

def create_character(name, weapon, strength, shield, bribe):
    characters[name] = {}
    characters[name]['weapon'] = weapon
    characters[name]['strength'] = strength
    characters[name]['bribe'] = bribe
    characters[name]['health'] = random.randint(50, 100)
    characters[name]['gold'] = random.randint(0, 100)
    characters[name]['healing'] = random.randint(0,50)
    characters[name]['status'] = "alive"

    if weapon:
        if outcome(0.5):
            characters[name]['weapon'] = "axe"
            characters[name]['strength'] += random.randint(30,60)
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

def heal_team(team):
    for player in team:
        if characters[player]['healing']:
            print(player + " drinks healing potion to restore their health ...")
            characters[player]['health'] += characters[player]['healing']
            characters[player]['healing'] = 0
            if characters[player]['health'] > 100:
                characters[player]['healing'] = characters[player]['health'] - 100 # remaining health potion
                characters[player]['health'] = 100

def add_suspense(time_to_sleep, debug):
    stdout.flush()
    if debug == False:
        time.sleep(time_to_sleep)

def generate_horde():
    if outcome(0.2): # 20% chance of spawning a MONSTER
        if outcome(0.1): horde = [create_character("Demon", False, 200, False, 0)]
        elif outcome(0.1): horde = [create_character("Dragon", False, 250, False, 0)]
        elif outcome(0.1): horde = [create_character("Giant ant", False, 80, False, 0)]
        elif outcome(0.1): horde = [create_character("Snake", False, 100, False, 0)]
        elif outcome(0.1): horde = [create_character("Cyclops", False, 200, False, 1000)]
        elif outcome(0.1): horde = [create_character("Gargoyle", False, 90, False, 0)]
        elif outcome(0.1): horde = [create_character("Goblin", False, 60, False, 500)]
        elif outcome(0.1): horde = [create_character("Spider", False, 80, False, 0)]
        elif outcome(0.1): horde = [create_character("Wolf", False, 70, False, 0)]
        elif outcome(0.1): horde = [create_character("Scorpion", False, 100, False, 0)]
        elif outcome(0.1): horde = [create_character("Ogre", False, 100, False, 200)]
        elif outcome(0.1): horde = [create_character("Minotaur", False, 150, False, 0)]
        elif outcome(0.1): horde = [create_character("Horseman", False, 100, False, 0)]
        elif outcome(0.1): horde = [create_character("Knight", False, 100, False, 500)]
        elif outcome(0.1): horde = [create_character("Medusa", False, 100, False, 0)]
        elif outcome(0.1): horde = [create_character("Cerberus", False, 100, False, 0)]
        else: horde = [create_character("Bat " + str(h), False, 30, False, 0) for h in range(0, 3)]
    else: # just spawn a horde of skeletons
        horde = [create_character("Skeleton " + str(h), outcome(0.4), random.randint(30,60), outcome(0.4), random.randint(30,60)) for h in range(0, random.randint(1,3))]

    return(horde)

def display_horde(horde):
    for npc in horde:
        if npc == "Demon": display_asciiart('demon')
        elif npc == "Dragon": display_asciiart('dragon')
        elif npc == "Giant ant": display_asciiart('giant_ant')
        elif npc == "Snake": display_asciiart('snake')
        elif npc == "Cyclops": display_asciiart('cyclops')
        elif npc == "Gargoyle": display_asciiart('gargoyle')
        elif npc == "Goblin": display_asciiart('goblin')
        elif npc == "Spider": display_asciiart('spider')
        elif npc == "Wolf": display_asciiart('wolf')
        elif npc == "Scorpion": display_asciiart('scorpion')
        elif npc == "Ogre": display_asciiart('ogre')
        elif npc == "Minotaur": display_asciiart('minotaur')
        elif npc == "Horseman": display_asciiart('horseman')
        elif npc == "Knight": display_asciiart('knight')
        elif npc == "Medusa": display_asciiart('medusa')
        elif npc == "Cerberus": display_asciiart('cerberus')
        elif npc.startswith("Bat "): display_asciiart('bats')
        else: 
            display_asciiart('skeleton')
