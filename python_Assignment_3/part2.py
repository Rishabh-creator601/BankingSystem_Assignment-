
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : 
@highest_level_attempted (P/C/D/HD):HD 

- Reflection:
- Reference:
"""

import random, csv ,sys ,time



DIRECTIONS = ["west","north","east","south"]


# functionality for reading csv file 
def read_csv(filename):
    try :
        with open(filename,"r") as f:
            data =  list(csv.reader(f))
            
        return data[1:]  # skipping header 
    except:
        print("[INFO]  FILE DOES NOT EXISTS ")


#you may use, extend and modify the following random generator
def generate_random_number(min =0, max_number = 1):
    r = random.randint(min,max_number)
    return r 

    

    
class Item:
    def __init__(self,name,desc,pickable,consumable):
        self.name =  name 
        self.desc = desc 
        self.pickable =  pickable
        self.consumable =  consumable
    
    
    def __repr__(self):
        return f"Item(<{self.name}>)"
                 
class Location:
    def __init__(self, name = "New room",desc=None, w = None, n = None , e = None, s = None):
        self._name = name
        self.desc = desc 
        self.doors = {"west":w,"east":e,"north":n,"south":s}
        self.creatures = []
        self.items = []
        
    def add_creature(self, creature):
        self.creatures.append(creature)
    
    def __repr__(self):
        return f"Location(<{self._name}>)"
    
    def add_item(self, item):
        self.items.append(item)
    
    def connect(self,direction,location):
        self.doors[direction] = location
        
        # connect back in opposite direction
        opposite = {"north": "south", "south": "north", "east": "west", "west": "east"}
        location.doors[opposite[direction]] = self
        
        
    def connect_east(self, another_room):
        self.connect("east",another_room)
        
    def connect_west(self, another_room):
        self.connect("west",another_room)
        
    def connect_north(self, another_room):
        self.connect("north",another_room)
        
    def connect_south(self, another_room):
        self.connect("south",another_room)
      
    @property    # getter 
    def name(self):
        return self._name
    
    @name.setter # setter 
    def name(self,new_name):
        self._name = new_name
    
    
    def express_location(self):
        print(f"You are at {self._name} , {self.desc} ")
    
    def add_item(self,itemObj: Item):
        
        self.items.append(itemObj)
    
    def express_items(self):
        for j in self.items:
            if j.pickable.strip() == "yes":
                print(f"Hi player , I am {j.name} ,{j.desc} ")
        
        

class Creature:
    def __init__(self,name,desc,location):
        self._name = name
        self.desc =  desc
        self._location  = location
        self.normal = False 
    
    @property
    def location(self):
        return self._location
    
    @property 
    def name(self):
        return self._name
    
    

    
    
    
class Pymon(Creature):
    def __init__(self, name = "Pymon name",desc= None , location=None):
        
        '''
        location :  A Location Object not a str 
        '''
        
        super().__init__(name,desc,location=location)
        self._current_location = location
        self._energy_count  =  3 
        self.total_energy_count =  3 
        self._speed =  7  # Inital speed taken if not given 
        self.inventory = []
        self.min_luck_factor  = 20 
        self.max_luck_factor =  50 
        self.race_range = 100 
        self.status_race =  "tie"
    
    def move(self, direction):
        if direction  in DIRECTIONS:
            
            new_location  =  self._current_location.doors.get(direction)
            
            #print("NEW LOCATION ENTERED : ",new_location)
            
            if isinstance(new_location,Location):  
                print(f"Moved from {self._current_location.name} TO {new_location.name}")
                self._current_location = new_location
            
            else:
                print("Player , You have No access to this direction !!")
            
        else:
            print("Player , You have No access to this direction !!")

                
     
    @property       
    def get_location(self):
        return self._current_location
    
    def __repr__(self):
        return f"Pymon(<{self._name}>)"
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self,new_value):
        self._speed =  new_value
    
    @property
    def energy(self):
        return self._energy_count
    
    @energy.setter
    def energy(self,new_count):
        self._energy_count =  new_count
    
    
    def express_urself(self):
        print(f"My name is {self._name}, I am a {self.desc} ,My energy level is  {self._energy_count}/{self.total_energy_count}")
    
    def pick_item(self,obj : Item):
        self.inventory.append(obj)
    
    def calculate_speed(self,luck_factor: int ,pos="pos"):
        
        # luck factor : percentage 
        # pos : ["neg","pos"]
        instant_speed = 0 
        
        if self.min_luck_factor  < luck_factor < self.max_luck_factor: 
            if pos  == "pos":
                instant_speed = self._speed + (luck_factor /100)  * self._speed
            else:
                instant_speed = self._speed -  (luck_factor /100) * self._speed
        else:
            print("Luck factor must be in range 20-50% ")
        
        return instant_speed
    
    def get_luck(self):
        
        luck =  random.choice(["neg","pos"])
        luck_factor =  generate_random_number(self.min_luck_factor,self.max_luck_factor)
        if luck  == "pos":
            
            instant_speed = self.calculate_speed(luck_factor,luck)
        else:
            instant_speed = self.calculate_speed(luck_factor,luck)
        return instant_speed
        

            
        
    def race(self,opp):
        
        
        print(f"\n🏁 Race started between {self._name} and {opp.name}!\n")
        
        distance_elapsed_own = 0.0
        distance_elapsed_opp = 0.0
        
        start = time.time()
        
        while True:
            
            
            time.sleep(1)
            elapsed = time.time() - start
            instant_speed =  self.get_luck()
            instant_speed_opp =  opp.get_luck()
            distance = instant_speed * elapsed
            distance_elapsed_own +=  distance
            
            distance_opp = instant_speed_opp * elapsed
            distance_elapsed_opp +=  distance_opp
            
            
            print(f"\n {self._name} (your Pymon) hopped {distance :.2f} meters. Distance remaining for {self._name}: {self.race_range -  distance_elapsed_own :.2f}  meters")
            print(f"{opp.name} (your Pymon) hopped {distance_opp :.2f} meters. Distance remaining for {opp.name}: {self.race_range -  distance_elapsed_opp :.2f}meters \n")
            
            
            if distance_elapsed_own >= self.race_range and distance_elapsed_opp >= self.race_range:
                print(" 🟰🟰 It's a tie! ")
                break
            elif distance_elapsed_own >= self.race_range:
                print(f"😎😎 {self._name} wins the race!")
                self.status_race =  "win"
                break
            elif distance_elapsed_opp >= self.race_range:
                print(f"☹️😔 {opp.name} wins the race!")
                self.status_race = "lose"
                self._energy_count -= 1 
                break
            
        
    
    def express_inventory(self):
        
        items_connect =  ",".join([item.name for item in self.inventory])
        print("You are carrying :",items_connect)
    
    def search_creature(self,name):
        Cobj  = None 
        for c in self._current_location.creatures:
            if c.name ==  name:
                Cobj =  c
                break 
        return Cobj
            
    
    
    def challenge_to_race(self,name :str ):
        
        if len(self._current_location.creatures) > 0 :
            
            cObj =  self.search_creature(name)
            if cObj != None  and cObj.normal == False:
                print("Creature challenged !")
                self.race(cObj)
            else:
                print(f"Cant challenge this creature : {name} !! ")
            


class Record:
    def __init__(self):
        locations_csv  = read_csv("locations.csv")
        creatures_csv  =read_csv("creatures.csv")
        items_csv = read_csv("items.csv")
        self.locations = {}
        self.creatures = {}
        self.item_list = []
        
    
        for location in locations_csv :
            name, desc, west , north, east, south =  location
            self.locations[name] =  Location(name=name,desc=desc,w=west,n=north,s=south,e=east)
    
            
        for creature in creatures_csv:
            name,desc,adoptable,speed =  creature
            normal =  True if adoptable.strip() == "no" else False
            self.creatures[name] = Pymon(name,desc=desc,location=None)
            self.creatures[name].speed =  float(speed) 
            self.creatures[name].normal = normal
        
        for item in items_csv:
            self.item_list.append(Item(item[0],item[1],item[2],item[3]) )   
    
    # fx for connecting location to a direction 
    def connect_loc(self,loc1,loc2,direction):
        if loc1 in self.locations.keys() and loc2 in self.locations.keys():
            if direction in DIRECTIONS:
                self.locations[loc1].connect(direction=direction,location=self.locations[loc2])
    
    # fx for placing creature to a location 
    def place_creature(self,name,location):
        
        if name in self.creatures.keys() and location in self.locations.keys():
            self.locations[location].add_creature(self.creatures[name])
        else:
            print(f"Either name : {name} ||  Location : {location} not found ")
    
    
    def place_item(self,loc_name,item_name):
        
        if loc_name in self.locations.keys() and self.search_item(item_name) != None :
            self.locations[loc_name].add_item(self.search_item(item_name))
            
    def search_item(self,name:str):
        
        itemObj = None
        for item in self.item_list:
            if item.name ==  name:
                itemObj =  item
                break 
        return itemObj
            
        
class Operations:
    def __init__(self):
        
        self.R = Record()
        ls =  self.R.locations
        self.curr_loc = ls[list(ls.keys())[generate_random_number(0, len(ls) - 1)]]
        
        self.current_pymon =  None 
        self.my_pymons = []
    
    def initial_setup(self):

        self.R.connect_loc("Playground","School","west")
        self.R.connect_loc("Playground","Beach","north")
        self.R.connect_loc("Beach","Playground","south")
        
        self.current_pymon  =  Pymon("Toromon","a white and yellow Pymon with a square face",self.R.locations["School"])
        self.my_pymons.append(self.current_pymon)
        
        self.R.place_creature("Kitimon","Playground")
        self.R.place_creature("Sheep","Beach")
        self.R.place_creature("Marimon","School")
        
        self.R.place_item("Playground","tree")
        self.R.place_item("Playground","potion")
        self.R.place_item("Beach","apple")
        self.R.place_item("School","binocular")
        
    
    def check_energy_status(self):
        
        
        for c in self.my_pymons:
            if c.energy == 0:
                self.my_pymons.remove(c)
                random_loc =  random.choice(list(self.R.locations.values()))
                random_loc.creatures.append(c)
                if self.my_pymons:
                    self.current_pymon = random.choice(self.my_pymons)
                else:
                    self.current_pymon = None       
                    print("No Pymons left in your team!")
                    print("GAME OVER !!")
                    sys.exit()
    
    def validate_None(self,text):

        if text != None and "None" not in text :
            return True 
        else:
            return False
    
    
    def inspect_pymon(self):
        
        print("1)  Inpect current pymon ")
        print("2)  List and select a benched Pymon to use.")
        
        user_input_inspect =  int(input("Enter what to inspect :"))
        
        try :
            
            if user_input_inspect ==  1:
                self.current_pymon.express_urself()
                
            elif user_input_inspect ==  2:
                
                
                print("You have available pymons :")
                for idx,c in enumerate(self.my_pymons):
                    print(f"{idx + 1})  {c.name}")
                
                py_input =  input("Enter name of pymon to use :")
                
                for idx,c in enumerate(self.my_pymons):
                    if c.name ==  py_input:
                        self.current_pymon = c 
                        print(f"You cuurent pymon is Now : {c.name}")
                        break 
        except ValueError:
            print("Please enter valid command !!")
    
        
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.curr_loc.name)
        print("You initally have toromon")
        self.current_pymon.express_urself()
        
        user_manuals = [
            "Inspect Pymon",
            "Inspect Current Location",
            "Move",
            "Pick an item",
            "View Inventory",
            "Challenge a Creature ",
            "Exit the program "
        ]
        print("Please issue a command to your Pymon :")
        
        for idx, manual in enumerate(user_manuals):
            print(f"{idx + 1}) {manual}")

        
        
        while True:
            
            
            try :
        
                user_input  = int(input("Your command : "))
                
                if user_input ==  1:
                    self.inspect_pymon()
                
                elif user_input == 2:
                    self.curr_loc.express_location()
                    
                    for  c in self.curr_loc.creatures:
                        c.express_urself()
                    
                    
                elif user_input == 3:
                    new_direction =  input("Moving to which direction  ? ").lower().strip()
                    self.current_pymon.move(new_direction)
                    self.curr_loc =  self.current_pymon.get_location
                
                elif user_input == 4 :
                    
                    if len(self.curr_loc.items) > 0:
                        self.curr_loc.express_items()
                        
                        item_input =  input("Picking what :")
                        itemObj =  self.R.search_item(item_input)
                        if itemObj != None:
                            self.current_pymon.pick_item(itemObj)
                            self.curr_loc.items.remove(itemObj)
                            print(f"You picked up {item_input} from the ground")
                    else:
                        print("No item left in the wild  !!")
                
                elif user_input ==  5:
                    self.current_pymon.express_inventory()
                
                elif user_input == 6:
                    creature_name =  input("Challenge who ? ")
                    
                    if creature_name != None and isinstance(creature_name,str) and creature_name != "":
                        self.current_pymon.challenge_to_race(creature_name)
                        if self.current_pymon.status_race == "win":
                            cObJ = self.current_pymon.search_creature(creature_name) # remove creature from location 
                            self.curr_loc.creatures.remove(cObJ) # and append it to our pet list 
                            self.my_pymons.append(cObJ)
                            print(f"You have Captured  {creature_name} !!")
                        self.check_energy_status()
                        
                
                elif user_input == int(len(user_manuals)) :
                    print("Exiting the Game !!")
                    sys.exit()
            
            except ValueError:
                print("Enter a Valid Argument !!")
        
        
        
## START FROM CHALLENGE A CREATURE stage 2 

O = Operations()
O.initial_setup()
O.start_game()


