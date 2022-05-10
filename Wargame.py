import random

#Good winds attack with one more dice
#Snow defends with one more dice
#Reinforcements adds +1 to attack
#Tactical support adds +1 to defense
cards = ["Snow","Snow","Good winds","Good winds","Normal","Normal","Normal","Normal","Tactical support","Tactical support","Reinforcements","Reinforcements"]

country = ["Argentina", "Terranova","Labrador","China","Japan","Russia","Germany","France","Italy","Spain","England","Iran"]

borders = {"Russia":["China","Japan","Iran"],"Japan":["Russia","China"],"China":["Iran","Russia","Japan"],"Iran":["China","Russia"],"Germany":["France","Italy","England"],"France":["Spain","Italy","England"],"England":["Spain","Germany","France"],
"Argentina":["Terranova","Labrador"],"Terranova":["Labrador","Argentina"],"Labrador":["Argentina","Terranova"]}

#Items in this list cannot attack again for the rest of the turn
not_attack = []
#and will move to this list when defending, recieving -1 to roll
defend = []

weaken = 0
counter = 0

def rules():
    print("Each current_player will roll a dice during an attack. The highest number wins and the current_player will conquer the country. When a current_player conquers the world, it's game over"
    "\nWhen the situation is Good Winds, attack has one more dice. With snow, defender rolls one more. Support will add +1 to defense, while Reinforcements will add +1 to attack"
    "\nIf an attack fails, that country cannot attack again for the rest of the turn, and will be weakened when defending with a -1 to defense\n")

def commands():
    print("You can use the 'attack' to attack the enemy. You can use 'check' to see list of countries owned, weak and can't attack. 'Pass' to end the turn. 'Rules' to see the rules")

rules()

player1_name = input("P1, what's your name?: ")
player2_name = input("P2, what's your name?: ")
print(f"Welcome {player1_name}\nWelcome {player2_name}\n")

#Distribution of countries
controlled_countries1 = random.sample(country,6)
print(f"{player1_name}, your countries are: ")
for n in controlled_countries1:
    print(n)
    country.remove(n)

controlled_countries2 = random.sample(country,6)
print(f"\n{player2_name}, your countries are: ")
for i in controlled_countries2:
    print(i)
    country.remove(i)


def weak():
    defend.clear()
    defend.extend(not_attack)
    not_attack.clear()

#a is for attacking; b is for defending
#c is for current_player
#d is for situation
#e is counter
def attack(a,b,c,d):
    print("You own:")
    for x in a:
        print(x)
    print(f"\nYou can't attack with:")
    for p in not_attack:
        print(p)
    #Declare the attack
    country_attack = input("\nChoose a country to attack with: ").capitalize()
    if country_attack not in a:
        print("You don't own that country")
    while country_attack in a:
        if country_attack in not_attack:
            print("You can't attack with that country anymore")
            break
        print("Your enemy owns:")
        for z in b:
            print(z)
        country_defend = input("\nChoose a country to attack: ").capitalize()
        if country_defend not in b:
            print("Enemy doesn't own that country")
        #Define if a country is within borders
        # if country_defend not in borders:
        #     print("Not a border")
        #     break
        while country_defend in b:
            #Dice A and B are the attacker's
            roll_diceA = random.randint(1,6)
            if d == "Good winds":
                roll_diceB = random.randint(1,6)
                print(f"Attacker got a {roll_diceA} and {roll_diceB}")
            elif d == "Reinforcements":
                roll_diceA = roll_diceA + 1
                print(f"Attacker got a {roll_diceA}")
            else: print(f"Attacker got a {roll_diceA}")

            #Dice C and D are the defender's
            roll_diceC = random.randint(1,6)
            if country_defend in defend:
                roll_diceC = roll_diceC - 1
            if d == "Snow":
                roll_diceD = random.randint(1,6)
                if country_defend in defend:
                    roll_diceD = roll_diceD - 1
                print(f"Defender got a {roll_diceC} and {roll_diceD}")
            elif d == "Tactical support":
                roll_diceC = roll_diceC + 1
                print(f"Defender got a {roll_diceC}")
            else: print(f"Defender got a {roll_diceC}")


            #Declare roll winner
            while d == "Normal" or d == "Reinforcements" or d == "Tactical support":
                if roll_diceA > roll_diceC:
                    print(f"{c} conquered {country_defend}")
                    global counter
                    counter += 1
                    a.append(country_defend)
                    b.remove(country_defend)
                    print(a)
                elif roll_diceA <= roll_diceC:
                    print(f"{country_defend} wins. {c} Can't attack with {country_attack} anymore!")
                    not_attack.append(country_attack)
                    counter += 1
                break

            while d == "Snow":
                if roll_diceA > roll_diceC and roll_diceD < roll_diceA:
                    print(f"{c} conquered {country_defend}")
                    counter += 1
                    a.append(country_defend)
                    b.remove(country_defend)
                    print(a)
                elif roll_diceA <= roll_diceC or roll_diceD >= roll_diceA:
                    print(f"{country_defend} wins. {c} Can't attack with {country_attack} anymore!")
                    not_attack.append(country_attack)
                    counter += 1
                break

            while d == "Good winds":
                if roll_diceA > roll_diceC or roll_diceC < roll_diceB:
                    print(f"{c} conquered {country_defend}")
                    counter += 1
                    a.append(country_defend)
                    b.remove(country_defend)
                    print(a)
                elif roll_diceA <= roll_diceC and roll_diceC >= roll_diceB:
                    print(f"{country_defend} wins. {c} Can't attack with {country_attack} anymore!")
                    not_attack.append(country_attack)
                    counter += 1
                break
            break

        break
#While counter is 3 to 5, if the current_player fails to guess the number all his countries will be moved to defend list and recieve a -1 to roll. If they guess it, they can attack again
#If the counter is equal or higher than 6, the current_player will have to guess twice if he wants to keep attacking. If he misses, he will recieve the -1 and skip his turn
def atk_limit(a,b):
    run = True
    while a > 2 and a < 5:
        gamble_question = input(f"You have already attacked {a} times. If you guess a number from 1 to 6, attack again. Else all your countries will recieve a -1 penalty: ").capitalize()
        if gamble_question == "Yes":
            while run:
                try:
                    gamble_dice = random.randint(1,6)
                    gamble = int(input("What's your number?(1 to 6): "))
                    if gamble < 1 or gamble > 6:
                        print("That's not a valid number")
                    else:
                        if gamble > 0 and gamble < 7:
                            if gamble == gamble_dice:
                                print("You guessed right. Attack again")
                                global weaken
                                weaken = 0
                                break
                            elif gamble != gamble_dice:
                                    print(f"Wrong!. The correct number was {gamble_dice}")
                                    weaken = 1
                                    defend.append(b)
                        break
                    break
                except ValueError:
                    print("Please write a number.")
            break
        elif gamble_question == "No":
            break
        else:
            print("Please choose yes or no")
    while a > 5:
        gamble_question = input(f"You have laready attacked {a} times. You have to guess twice to keep attacking. If you fail you will recieve a -1 penalty when defending and skip your next turn: ").capitalize()
        if gamble_question == "Yes":
            while run:
                try:
                    gamble_diceA = random.randint(1,6)
                    gamble_diceB = random.randint(1,6)
                    gambleA = int(input("What's your number?(1 to 6): "))
                    gambleB = int(input("What's your number?(1 to 6): "))
                    if gambleA < 1 or gambleA > 6 or gambleB < 1 or gambleB > 6:
                        print("That's not a valid number")
                    else:
                        if gambleA > 0 and gambleA < 7 and gambleB > 0 and gambleB < 7:
                            if gambleA == gamble_diceA and gambleB == gamble_diceB:
                                print("You guessed right. Attack again")
                                weaken = 0
                                break
                            elif gambleA != gamble_diceA or gambleB != gamble_diceB:
                                print(f"Wrong!. The correct numbers were {gamble_diceA} and {gamble_diceB}")
                                weaken = 1
                                defend.append(b)
                            break
                    break
                except ValueError:
                    print("Please write a number.")
            break
        elif gamble_question == "No":
            break
        else:
            print("Please choose yes or no")

def check(a,b):
    print(f"\n{player1_name} owns:")
    for i in controlled_countries1:
        print(i)
    print(f"\n{player2_name} owns:")
    for x in controlled_countries2:
        print(x)
    if len(not_attack) < 1:
        print("\nYou can attack with any country")
    else: print(f"\nYou can't attack with:")
    for p in not_attack:
        print(p)
    if len(defend) < 1:
        print("\nThere are no weak countries")
    else: print("\nThese countries are weak: ")
    for x in defend:
        print(x)
    print(f"\nCurrent situations is {a}")
    print(f"\nLimit counter is at {b}")

class Player():
    def __init__(self, name, controlled_countries):
        self.name = name
        self.controlled_countries = controlled_countries

class Country():
    def __init__(self, name, owner:Player, bordering_countries):
        self.name = name
        self.owner = owner
        self.bordering_countries = bordering_countries

player1 = Player(player1_name, controlled_countries1)
player2 = Player(player2_name, controlled_countries2)

players = [player1, player2]

country_dict = {}

def func_padre(players, country_owner):
    for player in players:
        variable = player if player.name == country_owner else None
        if variable:
            return variable
    return None

countries = [Country(country.name, func_padre(players, country.owner), country.bordering_countries) for country in country_dict]

for item, key in enumerate(players):
    print(item, key)

def main_game():
    turn = 0
    valid = True
    skip = True
    global counter
    while(valid):
        print("")
        while skip:
            situation = random.choice(cards)
            print(f"Current situation is: {situation} ")
            skip = False
            break
        # If turn = 0, Player 1 will play
        if turn == 0:
            current_player = player1
            global weaken
            if weaken == 1:
                turn = 1
        elif turn == 1:
            current_player = player2
            if weaken == 1:
                turn = 0
        atk_limit(counter,current_player.controlled_countries)
        commands()
        command = input(f"{current_player.name}, what do you want to do?: ").lower()
        if command == "attack":

            for player in players:
                if player.name != current_player.name:
                    defending_countries = player.controlled_countries

            attack(current_player.controlled_countries,defending_countries,current_player.name,situation)

            if turn == 0:
                attack(controlled_countries1,controlled_countries2,current_player.name,situation)
            elif turn == 1:
                attack(controlled_countries2,controlled_countries1,current_player.name,situation)
            #Check for winner. If any controlled_countries list is higher than x, said list current_player.name will win
            if len(controlled_countries1) > 11 or len(controlled_countries2) > 11:
                print(f"{current_player.name} conquered the world.")
                valid = False
        elif command == "check":
            check(situation,counter)
        elif command == "rules":
            rules()
        elif command == "pass":
            print(f"{current_player.name} ended the turn.")
            if turn == 0:
                weak()
                turn = 1
                counter = 0
                if weaken == 1:
                    defend.clear()
                    defend.append(controlled_countries1)
                    weaken = 0
            elif turn == 1:
                weak()
                turn = 0
                counter = 0
                if weaken == 1:
                    defend.clear()
                    defend.append(controlled_countries2)
                    weaken = 0
                skip = True
        else:
            print("Not a valid command")

main_game()
