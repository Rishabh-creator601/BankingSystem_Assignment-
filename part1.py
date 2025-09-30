

# ---------- GUEST  --------
class Guest:
    def __init__(self, guest_id, name):

        self.id = guest_id
        self.name = name
        self.reward_points  = 50 ## Initalized 50 points for each guest 
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
    def __init__(self, product_id, name, price,desc):
        super().__init__(product_id, name, price)
        self.desc= desc


    def display_info(self):
        print(f"Supplementary Item ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(self.desc)
        print(f"Price: {self.get_price()}")
        if self.__category:
            print(f"Category: {self.__category}")
        print(f"Stock Quantity: {self.__stock_quantity}")
        


SupplementaryItems = {
    "car_park":SupplementaryItem("car_park","Car Parking",25,"Car park for 1 car. (per night rate)"),
    "breakfast":SupplementaryItem("breakfast","Breakfast",21,"Continental breakfast meal. (per person)"),
    "toothpaste":SupplementaryItem("toothpaste","ToothPaste",5,"Toothpaste – generic brand (per tube)"),
    "extra_bed":SupplementaryItem("extra_bed","Extra Bed",50,"Removable extra bed that can fit up 2 people. (per item per night) ")
    }
        
# -------  Order -------------


class Order: 
    def __init__(self,guest_id:str,product_ids,quantity:int):
        
        self.guest_id =  guest_id
        self.product_ids =  product_ids
        self.quantity =  quantity
        self.total_cost = 0
        
    
    def compute_cost(self):

        for i in self.product_ids:
            self.total_cost +=  SupplementaryItems[i].get_price()
            
            


