import random
import pygame

class World:
    def __init__(self):
        self.environments = []

    def add_environment(self, environment):
        self.environments.append(environment)

    def get_environment(self, name):
        for environment in self.environments:
            if environment.name == name:
                return environment
        return None


    def move(self, direction):
        # Find the new environment in the specified direction
        new_environment = None
        if direction == "north":
            new_environment = self.current_environment.north
        elif direction == "east":
            new_environment = self.current_environment.east
        elif direction == "south":
            new_environment = self.current_environment.south
        elif direction == "west":
            new_environment = self.current_environment.west

        # Check if the new environment exists
        if new_environment is None:
            print("You can't go that way!")
            return

        # Update the current environment and display its description
        self.current_environment = new_environment
        print(self.current_environment.description)
        self.current_environment.display_info()

        # Check for a random encounter
        if random.random() < self.current_environment.encounter_rate:
            enemy = self.current_environment.get_random_enemy()
            combat(self.player, enemy)


    def play(self):
        self.player = create_player()
        self.current_environment = self.environments[0]
        print(f"Hello, {self.player.name}!")
        print(f"You are in {self.current_environment.name}.")
        print(f"{self.current_environment.description}")
        self.current_environment.display_info()
        while True:
            print("What would you like to do?")
            print("1. Move to a new environment")
            print("2. Check your inventory")
            print("3. Equip an Item")
            print("4. Display equipment")
            print("5. Quit the game")
            if(isinstance(self.current_environment,Inn)):
                print("Press I to talk with innkeeper")
                print("Press P to talk with Patron")
            choice = input("> ")
            if choice == "1":
                print("Which direction do you want to go? (north, east, south, or west)")
                direction = input("> ").lower()
                self.move(direction)
                # Check for a random encounter
                if random.random() < self.current_environment.encounter_rate:
                    enemy = self.current_environment.get_random_enemy()
                    combat(self.player, enemy)
            elif choice == "2":
                self.player.display_inventory()

            elif choice == "3":
                item_name = input("Which item do you want to equip? ")
                for i in self.player.inventory:
                    if item_name.lower() == i.name.lower():
                        self.player.equip_item(i)
            elif choice == "4":
                self.player.display_equipment()
            elif choice == "5":
                print("Thanks for playing!")
                break
            elif(isinstance(self.current_environment,Inn)):
                if choice == "I":
                    self.current_environment.talk_to("innkeeper",self.player)
                if choice == "P":
                    self.current_environment.talk_to("patron",self.player)





# Create a player class to store player information
class Player:
    def __init__(self, name,playerClass,startingItems=[]):
        self.name = name
        self.health = playerClass.health
        self.max_health = playerClass.max_health
        self.attack = playerClass.attack
        self.defense = playerClass.defense
        self.speed = playerClass.speed
        self.gold = 0
        self.inventory = startingItems
        self.playerClass = playerClass
        self.equipped_items = {}

    def display_stats(self):
        print(f"{self.name}'s Stats:")
        print(f"health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"Inventory: {self.inventory}")
        print()
    def display_inventory(self):
        print(f"{self.name}'s inventory:")
        for item in self.inventory:
            print(item.name)
    def display_equipment(self):
        for i in self.equipped_items:
            print(i + ":" + self.equipped_items[i].name)

    def equip_item(self,item):
        if item in self.equipped_items.values():
            print("That item is already equipped.")
            return
        if isinstance(item, Weapon):
            if "Weapon" in self.equipped_items:
                print("You can only equip one weapon at a time.")
                return
            self.equipped_items["Weapon"] = item
            self.inventory.remove(item)
            self.attack += item.attack_bonus
            print(f"You have equipped the {item.name}.")
        elif isinstance(item, Armor):
            if "Armor" in self.equipped_items:
                print("You can only equip one set of armor at a time.")
                return
            self.equipped_items["Armor"] = item
            self.inventory.remove(item)
            self.defense += item.defense_bonus
            print(f"You have equipped the {item.name}.")
        else:
            print("That item cannot be equipped.")

# Define a list of enemies for the player to encounter
enemies = [
    {"name": "Goblin", "health": 50, "attack": 5, "defense": 5, "gold": 10},
    {"name": "Orc", "health": 75, "attack": 10, "defense": 10, "gold": 25},
]

import pygame

class Environment:
    def __init__(self, name, description, encounter_rate, enemies=[], items=[], rest_bonus=2,image='inn1.png'):
        self.name = name
        self.description = description
        self.encounter_rate = encounter_rate
        self.image = image
        self.enemies = enemies if enemies else []
        self.items = items if items else []
        self.rest_bonus = rest_bonus
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def add_neighbour(self, direction, environment):
        if direction == "north":
            self.north = environment
            environment.south = self
        elif direction == "east":
            self.east = environment
            environment.west = self
        elif direction == "south":
            self.south = environment
            environment.north = self
        elif direction == "west":
            self.west = environment
            environment.east = self
    def display_exits(self):
        exits = []
        if self.north:
            exits.append("north")
        if self.east:
            exits.append("east")
        if self.south:
            exits.append("south")
        if self.west:
            exits.append("west")

        if exits:
            print("Exits:")
            for exit in exits:
                print(f"- {exit.capitalize()}")
            print()
        else:
            print("There are no visible exits from here.")

    def get_random_enemy(self):
        return random.choice(self.enemies)

    def get_random_item(self):
        return random.choice(self.items)

    def display_info(self):
        print(self.name)
        print(self.description)
        print()

        # Load and display the image
        pygame.init()
        screen = pygame.display.set_mode((500, 400))
        img = pygame.image.load(self.image)
        screen.blit(img, (0, 0))
        pygame.display.update()

        if self.enemies:
            print("Enemies:")
            for enemy in self.enemies:
                print(f"- {enemy['name']}")
            print()
        if self.items:
            print("Items:")
            for item in self.items:
                print(f"- {item}")
            print()
        self.display_exits()


class Inn(Environment):
    def __init__(self, name, description, hp_regen, items=None):
        super().__init__(name, description, 0.0,items=items)
        self.hp_regen = hp_regen
        self.conversation_options = {
            "innkeeper": {
                "greeting": "Welcome to our inn, weary traveler. Would you like a room for the night?",
                "room": "Certainly! Our rooms are cozy and comfortable. It will be {} gold pieces for the night. Would you like to proceed?",
                "thanks": "Thank you for choosing our inn. I hope you have a pleasant stay!",
                "farewell": "Farewell and safe travels!"
            },
            "patron": {
                "greeting": "Greetings, adventurer. Have you seen any interesting sights on your travels?",
                "story": "Ah, I remember the time when I journeyed to the forbidden forest. The trees were so thick you could barely see the sky...",
                "rumor": "Have you heard about the cursed temple in the mountains? They say it's guarded by fierce monsters and filled with treasure...",
                "farewell": "May your travels be safe and fruitful!"
            }
        }

    def rest(self, player):
        player.health += self.hp_regen
        print(f"You rest at the {self.name} and recover {self.hp_regen} HP.")

    def talk_to(self, person,player):
        options = self.conversation_options.get(person)
        if options:
            print(options["greeting"])
            while True:
                choice = input("What would you like to say? ")
                if choice.lower() == "room":
                    cost = self.rest_bonus * 10
                    print(options["room"].format(cost))
                    confirm = input("Proceed with the booking? (Y/N) ")
                    if confirm.lower() == "y":
                        print(options["thanks"])
                        self.rest(player)
                elif choice.lower() == "story":
                    print(options["story"])
                elif choice.lower() == "rumor":
                    print(options["rumor"])
                elif choice.lower() == "farewell":
                    print(options["farewell"])
                    break
                else:
                    print("Sorry, I don't understand. Could you repeat that?")
        else:
            print("Sorry, there's no one here by that name.")




class Warrior:
    def __init__(self):
        self.name = "Warrior"
        self.health = 20
        self.max_health = 20
        self.attack = 10
        self.defense = 8
        self.speed = 2

class Mage:
    def __init__(self):
        self.name = "Mage"
        self.health = 15
        self.max_health = 15
        self.attack = 4
        self.defense = 3
        self.speed = 3

class Rogue:
    def __init__(self):
        self.name = "Rogue"
        self.health = 18
        self.max_health = 18
        self.attack = 4
        self.defense = 3
        self.speed = 5


class Weapon:
    def __init__(self, name, attack_bonus):
        self.name = name
        self.attack_bonus = attack_bonus

class Armor:
    def __init__(self, name, defense_bonus):
        self.name = name
        self.defense_bonus = defense_bonus


basic_sword = Weapon("Sword",5)
basic_armor = Armor("Armor",5)

def create_player():
    print("Welcome, adventurer! Let's create your character.")
    name = input("What is your character's name? ")
    print("Choose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    class_choice = input("Enter the number of your class choice: ")
    while class_choice not in ["1", "2", "3"]:
        class_choice = input("Invalid choice. Enter the number of your class choice: ")
    if class_choice == "1":
        player_class = Warrior()
        starting_items = [basic_sword,basic_armor]
    elif class_choice == "2":
        player_class = Mage()
        starting_items = ["wand", "spellbook"]
    elif class_choice == "3":
        player_class = Rogue()
        starting_items = ["dagger", "thieves' tools"]
    player = Player(name, player_class, starting_items)
    return player


# Add the environments to the world
world = World()



inn = Inn("The Rusty Sword Inn", "A cozy inn with a roaring fireplace.", 10, items=["potion", "scroll"])
dungeon = Environment("Dungeon", "You are in a dank dungeon.", 0.3,enemies,image="dungeon1.png")
room1 = Environment("Room 1", "You are in a dusty room.", 0.1,enemies,image="dungeon2.png")
room2 = Environment("Room 2", "You are in a dark room.", 0.2,enemies)
hallway1 = Environment("Hallway 1", "You are in a dimly lit hallway.", 0.05,enemies)
hallway2 = Environment("Hallway 2", "You are in a narrow hallway.", 0.1,enemies)
exit_room = Environment("Exit Room", "You are in a room with a door.", 0.05,enemies)



inn.add_neighbour("north",dungeon)
dungeon.add_neighbour("north", room1)
room1.add_neighbour("south", dungeon)
room1.add_neighbour("north", hallway1)
hallway1.add_neighbour("south", room1)
hallway1.add_neighbour("north", room2)
hallway1.add_neighbour("east", hallway2)
hallway2.add_neighbour("west", hallway1)
room2.add_neighbour("south", hallway1)
room2.add_neighbour("east", exit_room)
exit_room.add_neighbour("west", room2)

world.add_environment(inn)
world.add_environment(dungeon)
world.add_environment(room1)
world.add_environment(room2)
world.add_environment(hallway1)
world.add_environment(hallway2)
world.add_environment(exit_room)


# Define a function for combat
def combat(player, enemy):
    print(f"You encounter a {enemy['name']}!")
    while player.health > 0 and enemy['health'] > 0:
        # Player's turn
        print(f"What do you want to do, {player.name}?")
        print("1. Attack")
        print("2. Defend")
        choice = input("> ")
        if choice == "1":
            damage = random.randint(player.attack // 2, player.attack)
            damage -= enemy['defense']
            if damage < 0:
                damage = 0
            enemy['health'] -= damage
            print(f"You deal {damage} damage to the {enemy['name']}!")
        elif choice == "2":
            player.defense += 5
            print(f"You brace yourself for the {enemy['name']}'s attack!")

        # Enemy's turn
        if enemy['health'] > 0:
            damage = random.randint(enemy['attack'] // 2, enemy['attack'])
            damage -= player.defense
            if damage < 0:
                damage = 0
            player.health -= damage
            print(f"The {enemy['name']} deals {damage} damage to you!")

        # Display stats
        player.display_stats()
        print(f"The {enemy['name']}'s health: {enemy['health']}\n")

    if player.health <= 0:
        print("You have been defeated!")
        quit()
    else:
        print(f"You defeated the {enemy['name']}!")
        player.gold += enemy['gold']
        player.display_stats()
        print(f"You gained {enemy['gold']} gold!\n")


# Game loop
world.play()
