
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : 
@highest_level_attempted (P/C/D/HD):

- Reflection:
- Reference:
"""

import random, csv ,sys 



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
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 

    
            
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
        self._speed =  1

    
    
    def move(self,direction):
        
        if direction in DIRECTIONS:
            if self._current_location.doors[direction] != None :
                print(f"{self._name} moved from {self._current_location.name} To {self._current_location[direction.name]}")
                self._current_location = self._current_location.doors[direction]
        else:
            print("No access to direction : ",direction)
                
     
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


class Record:
    def __init__(self):
        locations_csv  = read_csv("locations.csv")
        creatures_csv  =read_csv("creatures.csv")
        items_csv = read_csv("items.csv")
        self.locations = {}
        self.creatures = {}
    
        for location in locations_csv :
            name, desc, west , north, east, south =  location
            self.locations[name] =  Location(name=name,desc=desc,w=west,n=north,s=south,e=east)

            
        for creature in creatures_csv:
            name,desc,adoptable,speed =  creature
            normal =  True if adoptable == "no" else False
            self.creatures[name] = Pymon(name,desc=desc,location=None)
            self.creatures[name].speed =  speed 
            self.creatures[name].normal = normal 
                
        print(f"Added Locations : {list(self.locations.keys())}")
        print(f"Added Creatures : {list(self.creatures.keys())}")

    

    
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
    

            
        
class Operations:
    def __init__(self):
        
        self.R = Record()
        self.curr_loc =  self.R.locations["School"]
    
    def initial_setup(self):

        self.R.connect_loc("Playground","School","west")
        self.R.connect_loc("Playground","Beach","north")
        self.R.connect_loc("Beach","south","Playground")
        
        self.toromon  =  Pymon("Toronmon","a white and yellow Pymon with a square face",self.R.locations["School"])
        
        self.R.place_creature("Kitimon","Playground")
        self.R.place_creature("Sheep","Beach")
        self.R.place_creature("Marimon","School")
    
    def validate_None(self,text):

        if text != None and "None" not in text :
            return True 
        else:
            return False
    
        
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.curr_loc.name)
        print("You initally have toromon")
        self.toromon.express_urself()
        print("Please issue a command to your Pymon :")
        print("1) Inspect Pymon")
        print("2) Inspect Current Location")
        print("3) Move")
        print("4) Exit the program ")
        
        
        while True:
        
            user_input  = int(input("Your command : "))
            
            if user_input ==  1:
                print("Hi Player ,",end="")
                
                for c in self.curr_loc.creatures:
                    c.express_urself()
                
                print("What can I  do to help you ? ")
            
            elif user_input == 2:
                self.curr_loc.express_location()
                
                
            elif user_input == 3:
                dir = input("Moving to which direction? ").strip().lower()
                
                if dir in DIRECTIONS:
                    next_loc = self.curr_loc.doors.get(dir)
                    
                    if next_loc is None:
                        print("You have no access to this direction!!")
                    else:
                        # If next_loc is still a string (due to CSV issues), convert to Location object
                        if isinstance(next_loc, str):
                            next_loc = self.R.locations.get(next_loc.strip())
                            if next_loc is None:
                                print("Invalid location reference!")
                                continue
                        
                        self.curr_loc = next_loc
                        print(f"You travelled {dir} and arrived at {self.curr_loc.name}")
                else:
                    print(f"Direction '{dir}' is invalid.")
            
            elif user_input == 4 :
                print("Exiting the Game !!")
                sys.exit()
        
        
        

O = Operations()
O.initial_setup()
O.start_game()
