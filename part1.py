import csv



## Searching for file
file_status= False

try :
    with open("guests.csv","r") as f :
        file_status = True
        guests =  csv.reader(f)
        print("File Found and loaded ")
except :
    file_status = False
    print("⚠️⚠️ Warning : File not found , please insert it in local directory !!!")


# ---------- GUEST  --------
class Guest:
    def __init__(self, guest_id, name,reward_points):

        self.id = guest_id
        self.name = name
        self.reward_points  = reward_points ## Initalized 50 points for each guest 
        self.reward_rate = 1.0    
        self.redeem_rate = 0.01     

    # Method to calculate reward based on total cost
    def calculate_reward(self, total_cost):
        reward_points = round(total_cost * self.__reward_rate)
        return reward_points
        
    
    def get_reward(self,cost):
        self.reward_points += abs(cost * self.reward_rate)
    
    def update_reward(self,value):
        self.reward_points += value 
    
    def get_discount(self):
        discount  = self.reward_points * self.redeem_rate 
        return discount

    # Method to display guest information
    def display_info(self):
        print(f"ID: {self.__id}")
        print(f"Name: {self.__name}")
        print(f"Reward Points: {self.__reward}")
        print(f"Reward Rate: {self.__reward_rate * 100}%")
        print(f"Redeem Rate: {self.__redeem_rate * 100}%")


    def set_reward_rate(self, rate_percent):
        self.__reward_rate = rate_percent / 100.0


    def set_redeem_rate(self, rate_percent):
        self.__redeem_rate = rate_percent / 100.0
        





        
    
    
    

        

# ----------- Product ----------
class Product:
    def __init__(self, product_id, name, price):

        self.__id = product_id
        self.__name = name
        self.__price = price

    # Getter 
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    # Empty super method as in sheet 
    def display_info(self):
        pass


# ------------- Apartment Unit -------------
class ApartmentUnit(Product):
    def __init__(self, product_id, name, price, capacity):

        super().__init__(product_id, name, price)
        self.__capacity = capacity

    # Getter 
    def get_capacity(self):
        return self.__capacity

    def display_info(self):
        print(f"Apartment ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price per night: {self.get_price()}")
        print(f"Capacity: {self.__capacity} guests")

# --------------- Supplemetary Item ----------------
class SupplementaryItem(Product):
    def __init__(self, product_id, name, price):
        super().__init__(product_id, name, price)


    def display_info(self):
        print(f"Supplementary Item ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price: {self.get_price()}")
        if self.__category:
            print(f"Category: {self.__category}")
        print(f"Stock Quantity: {self.__stock_quantity}")
        

class Records :
    def __init__(self):
        self.Guests =  {}
        self.guests_list =  list(self.Guests.keys())
        
        self.SupplementaryItems = {}
        self.supp_list =  list(self.SupplementaryItems.keys())
        
        self.ApartmentUnits  = {}
        self.apt_list=  list(self.ApartmentUnits.keys())
        
    
    def read_csv(self,filename):

        with open("guests.csv","r") as f :

            guests_file =  csv.reader(f)
            for g in guests_file :
                g_id =  int(g[0])
                g_name =  g[1]
                g_r_rate =  int(g[2])
                g_r =  int(g[3])
                g_redeem_r = int(g[4])
                self.Guests[g_id] = Guest(g_id,g_name,g_r)
                self.Guests[g_id].set_reward_rate(g_r_rate)
                self.Guests[g_id].set_redeem_rate(g_redeem_r)
    
    def read_products(self,filename):
        with open("products.csv","r") as f:
            product_file =  csv.reader(f)
            for product in product_file:
                
                # for adding product like breakfast , car park
                if product[0].startswith("S"):
                    s_item  = product[0]
                    s_name =  product[1]
                    s_rate  = int(product[2])
                    self.SupplementaryItems[s_item] = SupplementaryItem(s_item,s_name,s_rate)
                    
                # for adding Apartment Unit like U12 , U20 etc 
                if product[0].startswith("U"):
                    a_item =  product[0]
                    a_name =  product[1]
                    a_price=  product[1]
                    a_capacity =  product[2]
                    self.ApartmentUnits[a_item]=  ApartmentUnit(a_item,a_name,a_price,a_capacity)
                    
                    
            
    
    
    def find_guest(self,id=None, name=None):
        
        
        # Guest found via id 
        if (id != None ) and id in self.guests_list:
            guest_found =  self.Guests[id]
        
        # Guest found via name 
        elif (name != None):
            for id_hover,guest_ in self.Guests.items():
                if guest_.name == name:
                    guest_found =  self.Guests[id_hover]
            
        return guest_found
    
    
    def list_guest(self):
        
        print("="*45)
        for id,g in self.Guests.items():
            print(f"""
Guest ID  : {id}
Name : {g.name}
Reward Points : {g.reward_points}
Redeem Rate :  {g.redeem_rate}
Reward Rate : {g.reward_rate}
                   
                  """)
            print("*"*40)
            
            
            

Guests  = Records().Guests
Guests.read_csv("guests.csv")
SupplementaryItems = Records().SupplementaryItems
SupplementaryItems.read_products("prodcuts.csv")

# -------  Order -------------


class Order: 
    def __init__(self,guest_id:str,product_ids,quantity:int):
        
        self.guest_id =  guest_id
        self.product_ids =  product_ids
        self.quantity =  quantity
        self.total_cost = 0
        self.discount  = 0
    
    def compute_cost(self):

        for i in self.product_ids:
            self.total_cost +=  SupplementaryItems[i].get_price()
        
        
        user =  Guests[self.guest_id]
        self.discount =  user.get_discount()
        user.update_reward(user.calculate_reward(self.total_cost))
        self.new_price =  self.total_cost -  self.discount
        
        return (self.total_cost,self.discount, self.new_price)
    
    





            
            
        
        
       
            
            


