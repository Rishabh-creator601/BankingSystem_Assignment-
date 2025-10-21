import csv
from datetime import datetime




'''
NAME : 
STUDENT ID : 
Highest level of attempted : All the requirements 
May misbehave in calcuation of reward points 

'''

def read_csv_file(filename):
    csvFile = None 
    with open(filename, mode ='r') as file:
        csvFile = csv.reader(file)
        data = list(csvFile)
    return data



## Searching for file
file_status= False

try :
    guests =  read_csv_file("guests.csv")
    if guests:
        print(" ✔️ File Found and loaded ")
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
'''
Apartment Units are :
- Swan  : 100 rooms 
- Goose :  100 rooms 
- Duck : 100 rooms 

'''
# apt rates from previous assignment 
apt_rates =  {"swan":95,
              "duck":106.7,
              "goose":145.2}

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



def generate_receipt(
    guest_name, number_of_guests,
    apartment_name, apartment_rate,
    checkin_date, checkout_date, nights,
    booking_date,
    apartment_sub_total,
    supplementary_items,  # list of tuples: (id, name, qty, unit_price)
    supp_sub_total,
    total_cost, reward_points, discount, final_total, earned_rewards
):
    print("="*80)
    print(f"Guest name: {guest_name}")
    print(f"Number of guests: {number_of_guests}")
    print(f"Apartment name: {apartment_name}")
    print(f"Apartment rate: $ {apartment_rate:.2f} (AUD)")
    print(f"Check-in date: {checkin_date}")
    print(f"Check-out date: {checkout_date}")
    print(f"Length of stay: {nights} (nights)")
    print(f"Booking date: {booking_date}")
    print(f"Sub-total: $ {apartment_sub_total:.2f} (AUD)")
    print("-"*80)
    print("Supplementary items")
    print(f"{'ID':<10}{'Name':<20}{'Qty':<10}{'Unit Price $':<15}{'Cost $':<10}")
    for (sid, name, qty, unit_price )in supplementary_items:
        print(f"{sid:<10}{name:<20}{qty:<10}{unit_price:<15.2f}")
    print(f"Sub-total: $ {supp_sub_total:.2f}")
    print("-"*80)
    print(f"Total cost: $ {total_cost:.2f} (AUD)")
    print(f"Reward points to redeem: {reward_points}")
    print(f"Discount based on points: $ {discount:.2f} (AUD)")
    print(f"Final total cost: $ {final_total:.2f} (AUD)")
    print(f"Earned rewards: {earned_rewards}")
    print("Thank you for your booking!")
    print("We hope you will have an enjoyable stay.")
    print("="*80)

        

class Records :
    def __init__(self):
        self.Guests =  {}
        self.guests_list =  list(self.Guests.keys())
        
        self.SupplementaryItems = {}
        self.supp_list =  list(self.SupplementaryItems.keys())
        
        self.ApartmentUnits  = {}
        self.apt_list=  list(self.ApartmentUnits.keys())
        
    
    def read_csv(self,filename):
        guests_file = read_csv_file(filename)
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

        product_file =  read_csv_file(filename)
        for product in product_file:
            
            # for adding product like breakfast , car park
            if product[0].startswith("S"):
                s_item  = product[0]
                s_name =  product[1]
                s_rate  = float(product[2])
                self.SupplementaryItems[s_item] = SupplementaryItem(s_item,s_name,s_rate)
                
            # for adding Apartment Unit like U12 , U20 etc 
            if product[0].startswith("U"):
                a_item = product[0]
                a_name = product[1]
                a_price = float(product[2]) 
                a_capacity = int(product[3])  # assuming 4th column is capacity
                self.ApartmentUnits[a_item] = ApartmentUnit(a_item, a_name, a_price, a_capacity)

                    
                    
            

    
    def find_guest(self,id=None, name=None):
        
        guest_found  = None 
        # Guest found via id 
        if (id != None ) and id in self.Guests:
            guest_found =  self.Guests[id]
        
        # Guest found via name 
        elif (name != None):
            for id_hover,guest_ in self.Guests.items():
                #print("Processing:",guest_.name)
                if guest_.name == name:
                    guest_found =  self.Guests[id_hover]
                    break 
            
        return guest_found
    
    def find_product(self,id=None, name=None):
        
        product_found  = None 
        # Guest found via id 
        if (id != None ) and id in self.supp_list:
            product_found =  self.SupplementaryItems[id]
        
        # Guest found via name 
        elif (name != None):
            for id_hover,product_ in self.SupplementaryItems.items():
                if product_.name == name:
                    product_found =  self.SupplementaryItems[id_hover]
            
        return product_found
        
    
    
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
        print("="*45)
    
    
    
    def list_products(self,product_type):
        
        if product_type == "apartment":
            print("="*45)
            for apt_id,apt in self.ApartmentUnits.items():
                apt.display_info()
                print("*"*45)
            print("="*45)
        else:
            print("="*45)
            for p_id,p in self.SupplementaryItems.items():
                p.display_info()
                print("*"*45)
            print("="*45)
            
            
            

R  = Records()
R.read_csv("guests.csv") ;  R.read_products("products.csv")
Guests  = R.Guests
SupplementaryItems = R.SupplementaryItems

# -------  Order -------------


class Order: 
    def __init__(self,guest_id,product_ids,quantity):
        
        self.guest_id =  guest_id
        self.product_ids =  product_ids
        self.quantity =  quantity
        self.total_cost = 0
        self.discount  = 0
    
    def compute_cost(self):

        for i in self.product_ids:
            print(i)
            self.total_cost +=  SupplementaryItems[i].get_price() * self.quantity
        
        
        user =  Guests[self.guest_id]
        self.discount =  user.get_discount()
        user.update_reward(user.calculate_reward(self.total_cost))
        self.new_price =  self.total_cost -  self.discount
        
        return (self.total_cost,self.discount, self.new_price)
    
    
class Operations:
    def __init__(self):
        pass
    
    
    def make_booking(self):
        
        
        
        
        
        self.guest_name = input("Enter guest name: ")
        self.num_guests = int(input("Enter number of guests: "))
        self.apartment_id = input("Enter apartment ID: ")
        self.check_in = input("Enter check-in date (YYYY-MM-DD): ")
        self.check_out = input("Enter check-out date (YYYY-MM-DD): ")
        self.length_stay =  int(input("Enter Stay Length (Ex :  5) : "))
        self.booking_date = input("Enter booking date (YYYY-MM-DD): ")
        self.supplementary_item_id = input("Enter supplementary item ID: ")
        self.supplementary_item_qty = int(input("Enter supplementary item quantity: "))
        
        
        user_exist =  R.find_guest(name=self.guest_name)
        
        
        if user_exist== None :
            g_id =  str(len(R.Guests) +  1)
            R.Guests[g_id] =  Guest(g_id,self.guest_name,self.num_guests*30)
            # print(self.apartment_id[3:])

            
            if self.apartment_id[3:] in apt_rates.keys():
                price =  apt_rates[self.apartment_id[3:]]
        
            R.ApartmentUnits[self.apartment_id] = ApartmentUnit(self.apartment_id,f"{self.apartment_id} Building ",price,self.num_guests)
            print(f"User registered succesfully with ID  : {g_id} and apartment ID : {self.apartment_id}")
        else:
            
            #  IF THE USER ALREADY EXSIST 
            print(f"Hi {self.guest_name} Welcome Back again !")
            
            
            for obj in Guests.values():
                if obj.name == self.guest_name:
                    print("YOUR CURRENT REWARD POINTS: ",obj.reward_points)
                    
                    
                    
            total_cost, discount, new_price =  Order(user_exist.id,[self.supplementary_item_id],self.supplementary_item_qty).compute_cost()
            
            apt_rate_ =  apt_rates[self.apartment_id[3:]]
            
            supp_item_  =  SupplementaryItems[self.supplementary_item_id]
      
            supp_item_tuple_ = [(self.supplementary_item_id,supp_item_.get_name(),self.supplementary_item_qty,supp_item_.get_price())]
            #nights = (datetime.strptime(self.check_out, "%Y-%m-%d") -datetime.strptime(self.check_in, "%Y-%m-%d")).days
            nights=  self.length_stay
            
            
            apt_sub_total =  apt_rate_ * nights 
            
            generate_receipt(
                guest_name=user_exist.name,
                number_of_guests=self.num_guests,
                apartment_name=self.apartment_id[3:],
                apartment_rate=apt_rate_,
                checkin_date=self.check_in,
                checkout_date=self.check_out,
                nights=nights ,
                booking_date=self.booking_date,
                apartment_sub_total=apt_sub_total,
                supplementary_items=supp_item_tuple_,
                supp_sub_total=total_cost,
                final_total=new_price,
                reward_points=user_exist.reward_points,
                discount=discount,
                total_cost=apt_rate_+total_cost,
                earned_rewards=user_exist.get_reward(apt_rate_ + total_cost)
            )
    def display_menu(self):
        while True:
            print("\n" + "="*40)
            print("🏨 Hotel Management System 🏨")
            print("="*40)
            print("1. Make a booking")
            print("2. Display existing guests")
            print("3. Display existing apartment units")
            print("4. Display existing supplementary items")
            print("5. Exit")
            print("="*40)

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.make_booking()
            elif choice == "2":
                R.list_guest()
            elif choice == "3":
                R.list_products("apartment")
            elif choice == "4":
                R.list_products("supplementary")
            elif choice == "5":
                print("Exiting program. Thank you!")
                break
            else:
                print("⚠️ Invalid choice. Please try again.")
            
            
    


Operations().display_menu()






    
    


            
        
    
