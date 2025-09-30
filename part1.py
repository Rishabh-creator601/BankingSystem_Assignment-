

# ---------- GUEST  --------
class Guest:
    def __init__(self, guest_id, name, reward):

        self.__id = guest_id
        self.__name = name
        self.__reward = reward
        self.__reward_rate = 1.0    
        self.__redeem_rate = 0.01     

    # Getter 
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_reward(self):
        return self.__reward

    def get_reward_rate(self):
        return self.__reward_rate

    def get_redeem_rate(self):
        return self.__redeem_rate

    # Method to calculate reward based on total cost
    def calculate_reward(self, total_cost):
        reward_points = round(total_cost * self.__reward_rate)
        return reward_points

    # Method to update reward points
    def update_reward(self, value):
        self.__reward += value

    # Method to display guest information
    def display_info(self):
        print(f"ID: {self.__id}")
        print(f"Name: {self.__name}")
        print(f"Reward Points: {self.__reward}")
        print(f"Reward Rate: {self.__reward_rate * 100}%")
        print(f"Redeem Rate: {self.__redeem_rate * 100}%")

    # Method to set reward rate
    def set_reward_rate(self, rate_percent):
        self.__reward_rate = rate_percent / 100.0

    # Method to set redeem rate
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
    def __init__(self, product_id, name, price, category=None, stock_quantity=0):
        super().__init__(product_id, name, price)
        self.__category = category
        self.__stock_quantity = stock_quantity

    # Getter 
    def get_category(self):
        return self.__category

    def get_stock_quantity(self):
        return self.__stock_quantity

    def update_stock(self, quantity):
        self.__stock_quantity += quantity

    def display_info(self):
        print(f"Supplementary Item ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price: {self.get_price()}")
        if self.__category:
            print(f"Category: {self.__category}")
        print(f"Stock Quantity: {self.__stock_quantity}")
        
        



